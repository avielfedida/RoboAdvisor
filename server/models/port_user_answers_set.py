from app.extensions import db
from models.enums.risk import Risk
from models.enums.algorithm import Algorithm


class PortUserAnswersSet(db.Model):
    __tablename__ = 'port_user_answers_set'

    user_id = db.Column(db.String, primary_key=True)
    ans_set_val = db.Column(db.String, primary_key=True)
    portfolios_date_time = db.Column(db.DateTime, primary_key=True)
    portfolios_algorithm = db.Column(db.Enum(Algorithm), primary_key=True)
    portfolios_risk = db.Column(db.Enum(Risk), primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['user_id'],
            ['users._id'],
        ),
        db.ForeignKeyConstraint(
            ['ans_set_val'],
            ['answers_sets.ans_set_val'],
        ),
        db.ForeignKeyConstraint(
            ['portfolios_date_time', 'portfolios_algorithm', 'portfolios_risk'],
            ['portfolios.date_time', 'portfolios.algorithm', 'portfolios.risk'],
        ),
    )