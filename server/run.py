from celery_tasks.clr import configure_celery
from app.factory import create_app
import os

def run():
    # from celery_tasks.worker_tasks import insert_price_data
    # insert_price_data()
    # exit()
    app = create_app()
    # configure_celery(app)
    app.run(host='localhost', port=5000, debug=True)


if __name__ == '__main__':
    run()
