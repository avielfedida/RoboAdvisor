import datetime

from sqlalchemy import inspect

from app.extensions import db

class Results(db.Model):
    __tablename__ = 'results'
    name = db.Column(db.String, primary_key=True)
    added_date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    notes = db.Column(db.JSON, nullable=True)

    @staticmethod
    def columns():
        return list(map(lambda c: c.key, inspect(__class__).attrs))

    def as_dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return ret

