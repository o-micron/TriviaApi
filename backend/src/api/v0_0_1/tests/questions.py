import unittest
import json
from jsonschema import validate
from models.Question import Question
from models.shared import db
from app import app, API_VERSION
from flask_expects_json import expects_json


class QuestionTest(unittest.TestCase):
    def test_questions_create(self):
        with app.app_context():
            json = {
                'id': 1001,
                'question': 'Will this test pass ?',
                'answer': 'hopefully, yes it will',
                'categoryId': 3,
                'difficultyId': 2
            }
            response = app.test_client().post('/api/{}/questions'.format(API_VERSION), json=json)
            data = response.get_json()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('success'), True)
            self.cached_question = data.get('question')
            self.assertEqual(self.cached_question.get('id'), 1001)
            self.assertEqual(self.cached_question.get('id'), json.get('id'))
            self.assertEqual(self.cached_question.get('question'), json.get('question'))
            self.assertEqual(self.cached_question.get('answer'), json.get('answer'))

    def test_questions_delete(self):
        with app.app_context():
            response = app.test_client().delete('/api/{}/questions/1001'.format(API_VERSION))
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
