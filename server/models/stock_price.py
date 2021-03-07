from app.extensions import db
from models.enums.asset_type import AssetType


class StockPrice(db.Model):
    # Define the table name
    __tablename__ = 'stocks_prices'

    # Set columns for the table
    ticker = db.Column('ticker', db.String, primary_key=True)
    date_time = db.Column('date_time', db.DateTime, primary_key=True)
    price = db.Column('price', db.Numeric)
    asset_type = db.Column('asset_type', db.Enum(AssetType))

    def as_dict(self):
        stock_price_as_dict = {
            'ticker': self.ticker,
            'date_time': self.date_time.strftime('%m-%d-%Y'),
            'price': str(self.price),
            'asset_type': self.asset_type.name
        }
        return stock_price_as_dict
