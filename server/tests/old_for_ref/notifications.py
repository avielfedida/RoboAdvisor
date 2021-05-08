import json
import unittest
from datetime import datetime

from tests.old_for_ref.test_base import TestBase
from tests.old_for_ref.utils import json_resp


class TradesTestCase(TestBase):

    def setUp(self):
        super(TradesTestCase, self).setUp()
        self.register_and_login()
        self.base += '/notifications'

    def new_notification(self):
        self.new_algorithm('sometitle')
        dt = datetime.now()
        from models.notification import Notifications
        n = Notifications(user_id=self.user_id, added_date=dt,
                          data=json.dumps({
                              'endpoint': 'algorithms',
                              'id': 'sometitle'
                          }))
        self.db.session.add(n)
        self.db.session.commit()
        return n

    def get_notifications(self):
        return self.client().get(self.base + '/',
                                 headers=self.headers)

    def delete_notification(self, nid):
        return self.client().delete(self.base + f'/{str(nid)}', headers=self.headers)

    def delete_all_notifications(self):
        return self.client().delete(self.base + '/', headers=self.headers)

    def test_get_notifications(self):
        res = self.get_notifications()
        self.assertEqual(200, res.status_code)
        self.assertEqual(len(json_resp(res)), 0)
        self.new_notification()
        res = self.get_notifications()
        self.assertEqual(200, res.status_code)
        self.assertEqual(len(json_resp(res)), 1)

    def test_delete_notification(self):
        res = self.delete_notification(datetime.now())
        self.assertEqual(404, res.status_code)
        notif = self.new_notification()
        res = self.delete_notification(notif.added_date)
        self.assertEqual(204, res.status_code)

    def test_delete_all_notifications(self):
        self.new_notification()
        self.new_notification()
        res = self.get_notifications()
        self.assertEqual(200, res.status_code)
        self.assertEqual(len(json_resp(res)), 2)
        res = self.delete_all_notifications()
        self.assertEqual(204, res.status_code)
        res = self.get_notifications()
        self.assertEqual(200, res.status_code)
        self.assertEqual(len(json_resp(res)), 0)


if __name__ == "__main__":
    unittest.main()
