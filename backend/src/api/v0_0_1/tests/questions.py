import unittest
import json
from jsonschema import validate
from models.Question import Question
from routes.question import QuestionRouter
from models.shared import db
from app import app, API_VERSION
from flask_expects_json import expects_json


class QuestionTest(unittest.TestCase):
    QUESTION_ID = 1001

    def test_questions_create(self):
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
        schema = {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'status': {'type': 'number'},
                'question': {
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
                            },
                            'required': ['id', 'name']
                        },
                        'difficulty': {
                            'type': 'object',
                            'properties': {
                                    'id': {'type': 'number'},
                                    'level': {'type': 'number'}
                            },
                            'required': ['id', 'level']
                        },
                    },
                    'required': ['id', 'creationDate', 'question', 'answer', 'category', 'difficulty']
                }
            },
            'required': ['success', 'status', 'question']
        }
        try:
            validate(data, schema)
        except Exception:
            self.assertTrue(False, msg="test_questions_create() schema is incorrect")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get('success'), True)
        q = data.get('question')
        self.assertEqual(q.get('id'), self.QUESTION_ID)
        self.assertEqual(q.get('id'), post_json.get('id'))
        self.assertEqual(q.get('question'), post_json.get('question'))
        self.assertEqual(q.get('answer'), post_json.get('answer'))

    def test_questions_search(self):
        # --------------------------------------------
        # post a question with exact question text
        # --------------------------------------------
        post_json = {
            'id': 1010,
            'question': 'Will this test pass ?',
            'answer': 'hopefully, yes it will',
            'categoryId': 3,
            'difficultyId': 2
        }
        url = '/api/{}/questions'.format(API_VERSION)
        app.test_client().post(url, json=post_json)
        # --------------------------------------------
        # now search for it
        # --------------------------------------------
        post_json = {
            'query': 'Will this test pass',
            'categoryId': 3
        }
        url = '/api/{}/questions/search'.format(API_VERSION)
        response = app.test_client().post(url, json=post_json)
        data = response.get_json()
        schema = {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'status': {'type': 'number'},
                'questions': {
                    'type': ['array', 'null'],
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
                                },
                                'required': ['id', 'name']
                            },
                            'difficulty': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'number'},
                                    'level': {'type': 'number'}
                                },
                                'required': ['id', 'level']
                            }
                        },
                        'required': ['id', 'creationDate', 'question', 'answer', 'category', 'difficulty']
                    }
                },
                'totalQuestions': {'type': 'number'},
                'currentCategory': {'type': 'string'}
            },
            'required': ['success', 'status', 'questions', 'totalQuestions', 'currentCategory']
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(len(data.get('questions')) > 0)
        self.assertTrue(data.get('totalQuestions') > 0)
        # delete the posted question
        app.test_client().delete('/api/{}/questions/1010'.format(API_VERSION))

    def test_questions_get_paginated(self):
        response = app.test_client().get('/api/{}/questions'.format(API_VERSION))
        data = response.get_json()
        schema = {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'status': {'type': 'number'},
                'questions': {
                    'type': ['array', 'null'],
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
                                },
                                'required': ['id', 'name']
                            },
                            'difficulty': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'number'},
                                    'level': {'type': 'number'}
                                },
                                'required': ['id', 'level']
                            }
                        },
                        'required': ['id', 'creationDate', 'question', 'answer', 'category', 'difficulty']
                    }
                },
                'totalQuestions': {'type': 'number'},
                'questionsPerPage': {'type': 'number'},
                'categories': {
                    'type': ['array', 'null'],
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'number'},
                            'name': {'type': 'string'}
                        },
                        'required': ['id', 'name']
                    }
                },
                'currentCategory': {'type': 'string'}
            },
            'required': ['success', 'status', 'questions', 'totalQuestions', 'questionsPerPage', 'categories', 'currentCategory']
        }
        try:
            validate(data, schema)
        except Exception:
            self.assertTrue(False, msg="test_questions_get_paginated() schema is incorrect")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(len(data.get('questions')) == QuestionRouter.QUESTIONS_PER_PAGE)
        self.assertTrue(data.get('totalQuestions') > 0)
        self.assertEqual(data.get('questionsPerPage'), QuestionRouter.QUESTIONS_PER_PAGE)
        self.assertTrue(len(data.get('categories')) > 0)

    def test_questions_get_all(self):
        response = app.test_client().get('/api/{}/questions/all'.format(API_VERSION))
        data = response.get_json()
        schema = {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'status': {'type': 'number'},
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
                                },
                                'required': ['id', 'name']
                            },
                            'difficulty': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'number'},
                                    'level': {'type': 'number'}
                                },
                                'required': ['id', 'level']
                            }
                        },
                        'required': ['id', 'creationDate', 'question', 'answer', 'category', 'difficulty']
                    }
                }
            },
            'required': ['success', 'status', 'questions']
        }
        try:
            validate(data, schema)
        except Exception:
            self.assertTrue(False, msg="test_questions_get_all() schema is incorrect")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(len(data.get('questions')) > 0)

    def test_questions_delete(self):
        url = '/api/{}/questions/{}'.format(API_VERSION, self.QUESTION_ID)
        response = app.test_client().delete(url)
        data = response.get_json()
        schema = {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'status': {'type': 'number'},
                'question': {
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
                            },
                            'required': ['id', 'name']
                        },
                        'difficulty': {
                            'type': 'object',
                            'properties': {
                                    'id': {'type': 'number'},
                                    'level': {'type': 'number'}
                            },
                            'required': ['id', 'level']
                        },
                    },
                    'required': ['id', 'creationDate', 'question', 'answer', 'category', 'difficulty']
                }
            },
            'required': ['success', 'status', 'question']
        }
        try:
            validate(data, schema)
        except Exception:
            self.assertTrue(False, msg="test_questions_delete() schema is incorrect")

        self.assertEqual(response.status_code, 202)
        self.assertEqual(data.get('success'), True)
        self.assertEqual(data.get('question').get('id'), 1001)
