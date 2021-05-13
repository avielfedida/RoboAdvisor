import unittest
from unittest.mock import patch
from werkzeug import exceptions
from tests.test_base import TestBase
import logging


class FormSubmitTestCase(TestBase):
    def setUp(self):
        super(FormSubmitTestCase, self).setUp()
        self.base += '/form_submit'
        self.model_name = 'markowitz'
        self.answers = {0: 2,
                        1: 2,
                        2: 2,
                        3: 2,
                        4: 2,
                        5: 2,
                        6: 2,
                        7: 2,
                        }

    def create_json_form_submit(self):
        json = {
            'model_name': self.model_name,
            'answers': self.answers
        }
        return json

    def create_response(self):
        json_form = self.create_json_form_submit()
        res = self.client().post(self.base + '/submit', headers=self.headers, json=json_form)
        return res

    def test_form_submit_correct_parameters(self):
        res = self.create_response()
        self.assertEqual(res.status_code, 200)

    def test_form_submit_wrong_model(self):
        self.model_name = 'aaa'
        res = self.create_response()
        self.assertEqual(res.status_code, 400)


    def test_form_submit_Q1_ans_not_in_range_of_0_to_5(self):
        self.answers[0] = -1
        res = self.create_response()
        self.assertEqual(res.status_code, 400)
        self.answers[0] = 6
        res = self.create_response()
        self.assertEqual(res.status_code, 400)

    def test_form_submit_Q2_ans_not_in_range_of_0_to_3(self):
        self.answers[1] = -1
        res = self.create_response()
        self.assertEqual(res.status_code, 400)
        self.answers[1] = 4
        res = self.create_response()
        self.assertEqual(res.status_code, 400)

    def test_form_submit_Q3_ans_not_in_range_of_0_to_2(self):
        self.answers[2] = -1
        res = self.create_response()
        self.assertEqual(res.status_code, 400)
        self.answers[2] = 3
        res = self.create_response()
        self.assertEqual(res.status_code, 400)

    def test_form_submit_Q4_ans_not_in_range_of_0_to_2(self):
        self.answers[3] = -1
        res = self.create_response()
        self.assertEqual(res.status_code, 400)
        self.answers[3] = 3
        res = self.create_response()
        self.assertEqual(res.status_code, 400)

    def test_form_submit_Q5_ans_not_in_range_of_0_to_4(self):
        self.answers[4] = -1
        res = self.create_response()
        self.assertEqual(res.status_code, 400)
        self.answers[4] = 5
        res = self.create_response()
        self.assertEqual(res.status_code, 400)

    def test_form_submit_Q6_ans_not_in_range_of_0_to_4(self):
        self.answers[5] = -1
        res = self.create_response()
        self.assertEqual(res.status_code, 400)
        self.answers[5] = 5
        res = self.create_response()
        self.assertEqual(res.status_code, 400)

    def test_form_submit_Q7_ans_not_in_range_of_0_to_4(self):
        self.answers[6] = -1
        res = self.create_response()
        self.assertEqual(res.status_code, 400)
        self.answers[6] = 5
        res = self.create_response()
        self.assertEqual(res.status_code, 400)

    def test_form_submit_Q8_ans_not_in_range_of_0_to_3(self):
        self.answers[7] = -1
        res = self.create_response()
        self.assertEqual(res.status_code, 400)
        self.answers[7] = 4
        res = self.create_response()
        self.assertEqual(res.status_code, 400)

    def test_form_submit_risk_resulting_is_minimal(self):
        self.answers[0] = 0
        res = self.create_response()
        self.assertEqual(res.status_code, 200)

    def test_form_submit_Sending_ID_does_not_exist(self):
        json = {
            'model_name': self.model_name,
            'answers': self.answers,
            'uid': '0'
        }
        res = self.client().post(self.base + '/submit', headers=self.headers, json=json)
        self.assertEqual(res.status_code, 400)

if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main()
