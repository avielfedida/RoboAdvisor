from app.extensions import db
from models.enums.risk import Risk


class AnswersSet(db.Model):
    __tablename__ = 'answers_sets'

    ans_1 = db.Column('ans_1', db.String, primary_key=True)
    ans_2 = db.Column('ans_2', db.String, primary_key=True)
    ans_3 = db.Column('ans_3', db.String, primary_key=True)
    ans_4 = db.Column('ans_4', db.String, primary_key=True)
    ans_5 = db.Column('ans_5', db.String, primary_key=True)
    ans_6 = db.Column('ans_6', db.String, primary_key=True)
    ans_7 = db.Column('ans_7', db.String, primary_key=True)
    ans_8 = db.Column('ans_8', db.String, primary_key=True)
    risk = db.Column('risk', db.Enum(Risk))

    def as_dict(self):
        answers_set_as_dict = {
            'ans_1': self.ans_1,
            'ans_2': self.ans_2,
            'ans_3': self.ans_3,
            'ans_4': self.ans_4,
            'ans_5': self.ans_5,
            'ans_6': self.ans_6,
            'ans_7': self.ans_7,
            'ans_8': self.ans_8,
            'risk': self.risk.name

        }
        return answers_set_as_dict
