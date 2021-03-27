from flask import current_app
from sqlalchemy import create_engine

from app.extensions import celery
from app.extensions import db
from pandas_datareader import data as pdr
import pandas as pd
from datetime import datetime, timedelta


@celery.task(name='print_hello', bind=True)
def print_hello(self):
    task_id = self.request.id
    print(f'Hello: {task_id}')
    return 'ans'


@celery.task(name='insert_price_data', bind=True)
def insert_price_data(self):
    print('start')
    task_id = self.request.id

    # setting time period of the stock prices (default is one year) //todo change time period
    end_date = datetime.now() - timedelta( days=1 )
    # start_date = datetime( end_date.year - 1, end_date.month, end_date.day )
    start_date = datetime( end_date.year, end_date.month, end_date.day - 1 )

    # getting bonds price data
    bonds = ['SHY', 'TLT', 'SHV', 'IEF', 'GOVT', 'BIL', 'IEI', 'VGSH', 'SCHO', 'VGIT', 'SCHR', 'SPTS', 'SPTL',
             'GBIL', 'SPTI', 'VGLT', 'TLH', 'EDV', 'USFR', 'SGOV', 'CLTL', 'BSJK', 'FLGV', 'ZROZ', 'TFLO']
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
    stocks = pd.read_html( 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies' )[0]['Symbol'].tolist()
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
        data_to_insert = data_to_insert[~data_to_insert['date_time'].isin(table_data['date_time'])]
    data_to_insert.to_sql( 'stocks_prices', db.engine, if_exists='append', index=False )
    print('done inserting assets data to the database')


