from app.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
import re


class AnswersSet(db.Model):
    __tablename__ = 'answers_sets'

    ans_set_val = db.Column('ans_set_val', db.String, primary_key=True) # like "1,1,1,1,1,1,1,1"
    ans_1 = db.Column('ans_1', db.String)
    ans_2 = db.Column('ans_2', db.String)
    ans_3 = db.Column('ans_3', db.String)
    ans_4 = db.Column('ans_4', db.String)
    ans_5 = db.Column('ans_5', db.String)
    ans_6 = db.Column('ans_6', db.String)
    ans_7 = db.Column('ans_7', db.String)
    ans_8 = db.Column('ans_8', db.String)
    risk = db.Column('risk', db.Integer)
    port_user_answers_set = relationship("PortUserAnswersSet", backref='ans_set')

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
            'risk': self.risk
        }
        return answers_set_as_dict

    # @validates('ans_set_val')
    # def validate_ans_set_val(self, key, ans_set_val):
    #     r = re.compile('.,.,.,.,.,.,.,.')
    #     if r.match(ans_set_val):
    #         return ans_set_val
