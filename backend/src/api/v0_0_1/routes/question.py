import json
from flask import jsonify
from routes.http_codes import http_okay
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty


class QuestionRouter:
    def get_all():
        questions = Question.query.order_by(Question.creation_date.asc()).all()
        categories = Category.query.order_by(Category.name.asc()).all()
        return http_okay({
            "questions": [q.question for q in questions],
            "totalQuestions": len(questions),
            "categories": [q.name for q in categories],
            "currentCategory": categories[0].name
        })
