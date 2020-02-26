import json
from flask import jsonify
from routes.http_codes import http_okay
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty


class QuestionRouter:
    def get_all():
        questions = Question.query.order_by(Question.question.asc()).all()
        return http_okay({
            "date": [q.format() for q in questions]
        })
