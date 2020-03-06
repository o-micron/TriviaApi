import unittest
import json
from models.Question import Question
from models.shared import db
from app import app, API_VERSION


class QuestionTest(unittest.TestCase):
    def test_questions_get_all(self):
        with app.app_context():
            response = app.test_client().get('/api/{}/questions/all'.format(API_VERSION))
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data.get('success'), True)
            self.assertTrue(len(data.get('questions')) > 0)


if __name__ == "__main__":
    unittest.main()
