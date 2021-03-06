import uuid

from sqlalchemy.exc import IntegrityError

from api.utils import get_next_answer_set_pk
from .clr import configure_celery
from celery.schedules import crontab
from celery.task import periodic_task

from app.extensions import db
from pandas_datareader import data as pdr
import pandas as pd
from datetime import datetime, timedelta

from app.factory import create_app

import os
from run import ROOT_DIR

app = create_app()
celery = configure_celery(app)


@celery.task(name='execute_rebalance', bind=True)
def execute_rebalance(self, link, user_id):
    with app.app_context():
        from models.portfolio import Portfolio
        from models.port_user_answers_set import PortUserAnswersSet
        from algorithms.create_model import create_model
        portfolio_by_algorithm = db.session.query(Portfolio).filter_by(link=link).first()
        algo = create_model(portfolio_by_algorithm.algorithm, portfolio_by_algorithm.risk)
        portfolio = algo.rebalance(link)
        db.session.add(portfolio)
        db.session.flush()
        for pk_of_risk in get_next_answer_set_pk(portfolio_by_algorithm.risk):
            pua = PortUserAnswersSet(user_id=user_id, ans_set_val=pk_of_risk, portfolios_id=portfolio.id,
                                        portfolios_date_time=portfolio.date_time)
            db.session.add(pua)
        db.session.commit()


@periodic_task(
    run_every=(crontab(minute=25, hour=15)),# Israel time = UTC + 3
    name="execute_models",
    ignore_result=True)
def execute_models():
    # Settings
    models_names = ['markowitz', 'Kmeans', 'blackLitterman', 'mean_gini']

    risks = range(1, 6)

    with app.app_context():
        from models.users import User
        from algorithms.create_model import create_model
        from models.portfolio import Portfolio
        from models.port_user_answers_set import PortUserAnswersSet

        uid = str(uuid.uuid4())
        user = User(_id=uid)
        db.session.add(user)

        for model_name in models_names:
            for risk in risks:
                model = create_model(model_name, risk)
                portfolio: Portfolio = model.get_portfolio_object()
                db.session.add(portfolio)
                db.session.flush()
                for pk_of_risk in get_next_answer_set_pk(risk):
                    pua = PortUserAnswersSet(user_id=uid, ans_set_val=pk_of_risk, portfolios_id=portfolio.id, portfolios_date_time=portfolio.date_time)
                    db.session.add(pua)
        db.session.commit()


@periodic_task(
    run_every=(crontab(minute=59, hour=14)),# Israel time = UTC + 3
    name="insert_price_data",
    ignore_result=True)
def insert_price_data():
    with app.app_context():
        # from models.users import User
        # users = db.session.query(User).all()#todo: remove
        # task_id = self.request.id
        # setting time period of the stock prices (default is one year) //todo change time period
        end_date = datetime.now() - timedelta(days=1)
        # start_date = datetime( end_date.year - 1, end_date.month, end_date.day )
        start_date = datetime(end_date.year-1, end_date.month, end_date.day)

        # getting bonds price data
        bonds = pd.read_csv(os.path.join(ROOT_DIR, 'api/resources/bonds_list.csv'))['Symbol'].values
        # bonds = pd.read_csv('api/resources/bonds_list.csv')['Symbol']
        bonds_df = pdr.get_data_yahoo( bonds, start_date, end_date )['Adj Close']
        data_to_insert = pd.DataFrame( columns=['ticker', 'date_time', 'price', 'asset_type', 'market_cap'] )
        for bond in bonds_df.columns:
            bond_data = pd.DataFrame()
            bond_data['date_time'] = bonds_df.index
            bond_data['price'] = bonds_df[bond].values
            bond_data['ticker'] = bond
            bond_data['asset_type'] = 'bond'
            try:
                marketCap = pdr.get_quote_yahoo( bond )['marketCap'][0]
            except:
                marketCap = int(0)
            bond_data['market_cap'] = [int(marketCap) for i in range( len( bond_data ) )]
            data_to_insert = data_to_insert.append( bond_data, ignore_index=True )
        data_to_insert['market_cap'].loc[data_to_insert['market_cap'] == 0] = [data_to_insert['market_cap'].mean() for i in range(len(data_to_insert['market_cap'].loc[data_to_insert['market_cap'] == 0]))]

        # getting stocks price data
        # stocks = pd.read_csv('api/resources/stocks_list.csv')['Symbol']
        stocks = pd.read_csv(os.path.join(ROOT_DIR, 'api/resources/stocks_list.csv'))['Symbol'].values

        stocks_df = pdr.get_data_yahoo( stocks, start_date, end_date )['Adj Close']
        for stock in stocks_df.columns:
            stock_data = pd.DataFrame()
            stock_data['date_time'] = stocks_df.index
            stock_data['price'] = stocks_df[stock].values
            stock_data['ticker'] = stock
            stock_data['asset_type'] = 'stock'
            try:
                marketCap = pdr.get_quote_yahoo( stock )['marketCap'][0]
            except:
                marketCap = int(0)
            stock_data['market_cap'] = [int(marketCap) for i in range( len( stock_data ) )]
            data_to_insert = data_to_insert.append( stock_data, ignore_index=True )

        # insert price data to sql table
        data_to_insert.dropna( inplace=True )
        if db.engine.dialect.has_table(db.engine, 'stocks_prices'):
            table_data = pd.read_sql_table('stocks_prices', db.engine)
            all_data = pd.concat([data_to_insert, table_data]).drop_duplicates(subset=['ticker', 'date_time'], keep=False)
            data_to_insert = all_data.loc[all_data['ticker'].isin(data_to_insert['ticker'])]
            data_to_insert = data_to_insert.loc[~(data_to_insert['date_time'].isin(table_data['date_time']))]
        data_to_insert.to_sql( 'stocks_prices', db.engine, if_exists='append', index=False )
        print('done inserting assets data to the database')



# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=22, minute=30),
#         insert_price_data.s(),
#     )