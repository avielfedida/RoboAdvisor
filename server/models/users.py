from app.extensions import db
from models.enums.sex import Sex
from models.enums.risk import Risk


class User(db.Model):
    # Define the table name
    __tablename__ = 'users'

    # Set columns for the table
    email = db.Column('email', db.String, primary_key=True)
    password = db.Column('password', db.String)
    first_name = db.Column('first_name', db.String)
    last_name = db.Column('last_name', db.String)
    age = db.Column('age', db.Numeric)
    sex = db.Column('sex', db.Enum(Sex))
    latest_portfolio_risk = db.Column('latest_portfolio_risk', db.Enum(Risk), default='undefined')

    def as_dict(self):
        user_as_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return user_as_dict
