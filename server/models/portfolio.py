from app.extensions import db
from models.enums.risk import Risk
from models.enums.algorithm import Algorithm


class Portfolio(db.Model):

    __tablename__ = 'portfolios'

    date_time = db.Column('date_time', db.DateTime, primary_key=True)
    algorithm = db.Column('algorithm', db.Enum(Algorithm), primary_key=True)
    risk = db.Column('risk', db.Enum(Risk), primary_key=True)
    link = db.Column('link', db.String)

    def as_dict(self):
        portfolio_as_dict = {
            'date_time': self.date_time.strftime('%m-%d-%Y'),
            'algorithm': self.algorithm.name,
            'risk': self.risk.name,
            'link': self.link
        }
        return portfolio_as_dict
