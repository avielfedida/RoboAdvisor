import eventlet
# This second import is due to: https://github.com/miguelgrinberg/flask-socketio/issues/309
import eventlet.wsgi

from app.factory import create_app


def run():
    app = create_app()
    # configure_celery(app)
    eventlet.monkey_patch()
    eventlet.wsgi.server(
        eventlet.listen(("localhost", 5000)), app)


if __name__ == '__main__':
    run()
