from app.extensions import db
from models.enums.gender import Gender
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
    gender = db.Column('gender', db.Enum(Gender))
    latest_portfolio_risk = db.Column('latest_portfolio_risk', db.Enum(Risk), default='undefined')

    def as_dict(self):
        user_as_dict = {
            'email': self.email,
            'first_name' : self.first_name,
            'last_name': self.last_name,
            'age': str(self.age),
            'gender': self.gender.name,
            'latest_portfolio_risk': self.latest_portfolio_risk.name
        }
        return user_as_dict
