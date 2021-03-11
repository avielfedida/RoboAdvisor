from re import error

from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    # Define the table name
    __tablename__ = 'users'

    # Set columns for the table
    _id = db.Column(db.String, primary_key=True)
    member = db.relationship('Member', backref='user', uselist=False)

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
