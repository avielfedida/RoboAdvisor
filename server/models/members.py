from app.extensions import db
from models.enums.gender import Gender
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class Member(db.Model):
    # Define the table name
    __tablename__ = 'members'

    # Set columns for the table
    email = db.Column('email', db.String, primary_key=True)
    password = db.Column('password', db.String)
    first_name = db.Column('first_name', db.String)
    last_name = db.Column('last_name', db.String)
    date_of_birth = db.Column('date_of_birth', db.String)
    # gender = db.Column('gender', db.Enum(Gender))
    latest_portfolio_risk = db.Column('latest_portfolio_risk', db.Integer, default=0)
    user_id = db.Column('user_id', db.String, db.ForeignKey('users._id'))
    topics = relationship("Topic", backref='member')
    messages = relationship("Message", backref='member')
    passwords_recovery = relationship("PasswordRecovery", backref='member')

    def __init__(self, email, password, first_name, last_name, date_of_birth, user_id):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.user_id = user_id

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        if not email or not password:
            return None
        member = cls.query.filter_by(email=email).first()
        if not member or not check_password_hash(member.password, password):
            return None
        return member

    def as_dict(self):
        member_as_dict = {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': str(self.date_of_birth),
            # 'gender': self.gender.name,
            'latest_portfolio_risk': self.latest_portfolio_risk,
            'user_id': self.user_id
        }
        return member_as_dict

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        return email
