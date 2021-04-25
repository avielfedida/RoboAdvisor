import uuid

from .clr import configure_celery
from celery.schedules import crontab
from celery.task import periodic_task

from app.extensions import db
from pandas_datareader import data as pdr
import pandas as pd
from datetime import datetime, timedelta

from app.factory import create_app


app = create_app()
celery = configure_celery(app)


@celery.task(name='print_hello', bind=True)
def print_hello(self):
    task_id = self.request.id
    print(f'Hello: {task_id}')
    return 'ans'



def get_next_answer_set_pk(only_risk_of):
    for risk in range(1, 5 + 1):
        if risk != only_risk_of:
            continue
        for ans_1 in range(1, 6 + 1):
            for ans_2 in range(1, 4 + 1):
                for ans_3 in range(1, 3 + 1):
                    for ans_4 in range(1, 3 + 1):
                        for ans_5 in range(1, 5 + 1):
                            for ans_6 in range(1, 5 + 1):
                                for ans_7 in range(1, 5 + 1):
                                    for ans_8 in range(1, 4 + 1):
                                        yield "{}_{}_{}_{}_{}_{}_{}_{}_{}".format(risk, ans_1, ans_2, ans_3,
                                                                                                 ans_4, ans_5, ans_6,
                                                                                                 ans_7, ans_8)


@periodic_task(
    run_every=(crontab(minute=30, hour=12)),# Israel time = UTC + 3
    name="execute_models",
    ignore_result=True)
def execute_models():
    # Settings
    # models_names = ['blackLitterman']
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
    run_every=(crontab(minute=23, hour=9)),# Israel time = UTC + 3
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
        start_date = datetime(end_date.year, end_date.month-1, end_date.day)

        # getting bonds price data
        bonds = pd.read_csv('api/resources/bonds_list.csv')['Symbol']
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
        stocks = pd.read_csv('api/resources/stocks_list.csv')['Symbol']

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