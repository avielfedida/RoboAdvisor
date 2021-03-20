from app.extensions import db
from models.enums.gender import Gender
from models.enums.risk import Risk
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship


class Member(db.Model):
    # Define the table name
    __tablename__ = 'members'

    # Set columns for the table
    email = db.Column('email', db.String, primary_key=True)
    password = db.Column('password', db.String)
    first_name = db.Column('first_name', db.String)
    last_name = db.Column('last_name', db.String)
    age = db.Column('age', db.Numeric)
    gender = db.Column('gender', db.Enum(Gender))
    latest_portfolio_risk = db.Column('latest_portfolio_risk', db.Enum(Risk), default='undefined')
    user_id = db.Column('user_id', db.String, db.ForeignKey('users._id'))
    topics = relationship("Topic", backref='member')
    messages = relationship("Message", backref='member')

    def as_dict(self):
        member_as_dict = {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': str(self.age),
            'gender': self.gender.name,
            'latest_portfolio_risk': self.latest_portfolio_risk.name,
            'user_id': self.user_id
        }
        return member_as_dict

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        return email
