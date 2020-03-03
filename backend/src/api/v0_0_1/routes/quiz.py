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
            'previous_questions': {'type': 'array'}
        },
        'required': ['categories', 'previous_questions']
    }

    def get_next_question(json_data):
        categories = json_data.get('categories')
        previous_questions = json_data.get('previous_questions')
        questions = Question.query.order_by(Question.creation_date.asc()).all()
        def f1(q): return q.category_id in [c.get('id') for c in categories]
        def f2(q): return q.id not in [pq.get('id') for pq in previous_questions]
        questions = list(filter(lambda q: f1(q) and f2(q), questions))
        if len(questions) > 0:
            remaining_questions = len(questions) - 1
            random.shuffle(questions)
            return http_okay({
                "question": questions[0].format(),
                "remaining_questions": remaining_questions
            })
        return http_error_404({"hint": "no question left available for the given category"})
