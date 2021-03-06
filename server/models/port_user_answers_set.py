from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.extensions import db
from models.answers_set import AnswersSet
from models.portfolio import Portfolio
from models.users import User


class PortUserAnswersSet(db.Model):
    __tablename__ = 'port_user_answers_set'

    user_id = db.Column(db.String, primary_key=True)
    ans_set_val = db.Column(db.String, primary_key=True)
    portfolios_id = db.Column(db.Integer, primary_key=True)
    portfolios_date_time = db.Column(db.DateTime)

    __table_args__ = (
        db.ForeignKeyConstraint(
            (user_id,),
            [User._id],
        ),
        db.ForeignKeyConstraint(
            (ans_set_val,),
            [AnswersSet.ans_set_val],
        ),
        db.ForeignKeyConstraint(
            (portfolios_id,),
            [Portfolio.id],
        ),
    )
