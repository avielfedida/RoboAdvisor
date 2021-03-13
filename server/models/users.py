from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    # Define the table name
    __tablename__ = 'users'

    # Set columns for the table
    _id = db.Column(db.String, primary_key=True)
    member = db.relationship('Member', backref='user', uselist=False)
    port_user_answers_set = db.relationship("PortUserAnswersSet", backref='user')

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        if not email or not password:
            return None
        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None
        return user

    def to_dict(self):
        return dict(email=self.email)

    def as_dict(self):
        user_as_dict = {
            'id': self._id,
        }
        return user_as_dict

    @hybrid_property
    def id(self):
        return self._id

    @id.setter
    def id(self, email):
        self._id = email
