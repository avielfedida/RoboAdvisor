import time

from celery import states
from requests import get

from tests.old_for_ref.test_base import TestBase


class CeleryXTest(TestBase):

    def __init__(self, *args, **kwargs):
        super(CeleryXTest, self).__init__(*args, **kwargs)
        self.base = self.base + '/api/v1'

    # def setUp(self):
    #     print('hi')
    #     # super(CeleryXTest, self).setUp()
    #     # self.resp = get(self.base + '/').json()

    def test_task_id_returned(self):
        assert 'task_id' in get(self.base + '/').json()


    def test_task_executed_and_finished(self):
        resp = get(self.base + '/').json()
        task_id = resp.get('task_id')
        interval = 3
        limit = 5
        state = None
        for i in range(limit):
            time.sleep(interval)
            resp1 = get(self.base + '/{}'.format(task_id))
            state = resp1.json().get('state')
        assert state == states.SUCCESS

# # base = 'http://127.0.0.1:5000/api/v1'
# # ns_cats = base + '/prefix/of/ns1'
# # resp = get(ns_cats + '/')
# # js = resp.json()
# print('Task submitted, ', js)
#
#
# def printit(task_id):
#     resp1 = get(ns_cats + '/{}'.format(task_id))
#     js = resp1.json()
#     print('Resp: ', js)
#     if js.get('state') == states.PENDING:
#         threading.Timer(3.0, lambda: printit(task_id)).start()
#
#
# printit(js.get('task_id'))
