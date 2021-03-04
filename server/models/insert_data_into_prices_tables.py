import pandas as pd
import datetime
from sqlalchemy import Table, Column, MetaData, create_engine, DateTime, Float
from sqlalchemy.orm import mapper, create_session


class Prices(object):
    __tablename__ = 'prices'
    pass

res = pd.read_excel('./assets_prices.xlsx', index_col=0)
cols = list(res.columns)
e = create_engine('postgresql+psycopg2://postgres:16941694@127.0.0.1:5432/robo_advisor')
session = create_session(bind=e, autocommit=False, autoflush=True)
