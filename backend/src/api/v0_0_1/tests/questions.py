import unittest
import json
from jsonschema import validate
from models.Question import Question
from models.shared import db
from app import app, API_VERSION
from flask_expects_json import expects_json


class QuestionTest(unittest.TestCase):
    QUESTION_ID = 1001

    def test_questions_create(self):
        with app.app_context():
            post_json = {
                'id': 1001,
                'question': 'Will this test pass ?',
                'answer': 'hopefully, yes it will',
                'categoryId': 3,
                'difficultyId': 2
            }
            url = '/api/{}/questions'.format(API_VERSION)
            response = app.test_client().post(url, json=post_json)
            data = response.get_json()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('success'), True)
            q = data.get('question')
            self.assertEqual(q.get('id'), self.QUESTION_ID)
            self.assertEqual(q.get('id'), post_json.get('id'))
            self.assertEqual(q.get('question'), post_json.get('question'))
            self.assertEqual(q.get('answer'), post_json.get('answer'))

    def test_questions_delete(self):
        with app.app_context():
            url = '/api/{}/questions/1001'.format(API_VERSION, self.QUESTION_ID)
            response = app.test_client().delete(url)
            data = response.get_json()
            self.assertEqual(response.status_code, 202)
            self.assertEqual(data.get('success'), True)

    def test_questions_get_all(self):
        with app.app_context():
            response = app.test_client().get('/api/{}/questions/all'.format(API_VERSION))
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data.get('success'), True)
            self.assertTrue(len(data.get('questions')) > 0)
            schema = {
                'type': 'object',
                'properties': {
                    'questions': {
                        'type': ['array', "null"],
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'number'},
                                'creationDate': {'type': 'string'},
                                'question': {'type': 'string'},
                                'answer': {'type': 'string'},
                                'category': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'number'},
                                        'name': {'type': 'string'}
                                    }
                                },
                                'difficulty': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'number'},
                                        'level': {'type': 'number'}
                                    }
                                }
                            },
                            'required': ['id', 'creationDate', 'question', 'answer', 'category', 'difficulty']
                        }
                    }
                },
                'required': ['questions']
            }
            try:
                validate(data, schema)
                self.assertTrue(True)
            except Exception:
                self.assertTrue(False)
