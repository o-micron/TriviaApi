import random
import json
from flask import jsonify, request
from routes.http_codes import http_okay, http_created, http_not_modified, http_deleted, http_error, http_error_400, http_error_404
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty


class QuizRouter:
    next_question_schema = {
        'type': 'object',
        'properties': {
            'categories': {'type': 'array'},
            'previousQuestions': {'type': 'array'}
        },
        'required': ['categories', 'previousQuestions']
    }

    def get_next_question(json_data):
        categories = json_data.get('categories')
        previous_questions = json_data.get('previousQuestions')
        questions = Question.query.order_by(Question.creation_date.asc()).all()
        def f1(q): return q.category_id in [c.get('id') for c in categories]
        def f2(q): return q.id not in previous_questions
        questions = list(filter(lambda q: f1(q) and f2(q), questions))
        next_question = None
        remaining_questions = 0
        if len(questions) > 0:
            remaining_questions = len(questions) - 1
            random.shuffle(questions)
            next_question = questions[0].format()
        return http_okay({
            "question": next_question,
            "remainingQuestions": remaining_questions
        })
