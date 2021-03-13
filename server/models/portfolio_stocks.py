from app.extensions import db
from models.enums.risk import Risk
from models.enums.algorithm import Algorithm


class PortfolioStocks(db.Model):
    __tablename__ = 'portfolio_stocks'

    stock_price_ticker = db.Column(db.String, primary_key=True)
    stock_price_date_time = db.Column(db.DateTime)
    portfolios_date_time = db.Column(db.DateTime, primary_key=True)
    portfolios_algorithm = db.Column(db.Enum(Algorithm), primary_key=True)
    portfolios_risk = db.Column(db.Enum(Risk), primary_key=True)
    weight = db.Column(db.Numeric)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['stock_price_ticker', 'stock_price_date_time'],
            ['stocks_prices.ticker', 'stocks_prices.date_time'],
        ),
        db.ForeignKeyConstraint(
            ['portfolios_date_time', 'portfolios_algorithm', 'portfolios_risk'],
            ['portfolios.date_time', 'portfolios.algorithm', 'portfolios.risk'],
        ),
    )
