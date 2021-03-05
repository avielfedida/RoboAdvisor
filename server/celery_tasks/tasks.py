from app.extensions import celery
from app.extensions import db
from models.number_addition import NumberAddition


@celery.task(name='tasks.execute_analysis', bind=True)
def execute_analysis(self, numA, numB):
    task_id = self.request.id
    res = numA + numB
    an = NumberAddition(numA=numA, numB=numB, result=res, task_id=task_id)
    db.session.add(an)
    db.session.commit()
