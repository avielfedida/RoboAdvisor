from celery_tasks.clr import configure_celery
from app.factory import create_app


def run():
    # from celery_tasks.tasks import print_hello
    # print_hello()
    app = create_app()
    # configure_celery(app)
    app.run(host='localhost', port=5000, debug=True)


if __name__ == '__main__':
    run()
