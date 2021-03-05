import datetime

from sqlalchemy import inspect

from app.extensions import db

class NumberAddition(db.Model):
    __tablename__ = 'number_addition'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    numA = db.Column(db.Integer)
    numB = db.Column(db.Integer)
    result = db.Column(db.Integer)
    task_id = db.Column(db.String)

    @staticmethod
    def columns():
        return list(map(lambda c: c.key, inspect(__class__).attrs))

    def as_dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return ret

