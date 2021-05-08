import json
import unittest

from tests.old_for_ref.test_base import TestBase
from tests.old_for_ref.utils import json_resp




class CombinationsTestCase(TestBase):

    def setUp(self):
        super(CombinationsTestCase, self).setUp()
        self.register_and_login()
        self.base += '/combinations'

    def new_combination(self):
        from models.combinations import Combinations
        res = self.study_first_step("XAR", "15min time frame")
        token = json_resp(res).get('token')
        res = self.study_submit([], 'somescriptname', token)
        study_id = json_resp(res).get('id')
        comb = Combinations(study_id=study_id, combination=json.dumps({'x': 4}), description=json.dumps("hi"))
        self.db.session.add(comb)
        self.db.session.commit()
        return comb

    def update_combination(self, comb_id, description, techniques):
        return self.client().patch(self.base + f'/{comb_id}', headers=self.headers, json={
            'description': description,
            'techniques': techniques
        })

    def test_update_technique(self):
        comb_id = self.new_combination().id
        print(comb_id)
        t1, t2 = 'ADXv2', 'RSIv3'
        self.new_tech(t1)
        self.new_tech(t2)
        res = self.update_combination(341412412, "desc...",
                                      [
                                          {'title': t1},
                                          {'title': t2}
                                      ])
        self.assertEqual(404, res.status_code)
        res = self.update_combination(comb_id, "desc...",
                                      [
                                          {'title': 'eqwe'},
                                          {'title': t2}
                                      ])
        self.assertEqual(404, res.status_code)
        res = self.update_combination(comb_id, "desc...",
                                      [
                                          {'title': t1},
                                          {'title': t2}
                                      ])
        self.assertEqual(204, res.status_code)



if __name__ == "__main__":
    unittest.main()
