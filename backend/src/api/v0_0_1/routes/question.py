import json
from flask import jsonify, request
from routes.http_codes import http_okay
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty

QUESTIONS_PER_PAGE = 5


class QuestionRouter:
    def get_all():
        page = request.args.get("page", default=1, type=int)
        questions = Question.query.order_by(Question.creation_date.asc())
        questions = questions.paginate(page, QUESTIONS_PER_PAGE, False).items
        categories = Category.query.order_by(Category.name.asc()).all()
        return http_okay({
            "questions": [q.format() for q in questions],
            "totalQuestions": len(questions),
            "categories": [q.name for q in categories],
            "currentCategory": categories[0].name
        })
