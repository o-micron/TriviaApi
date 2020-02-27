import json
from flask import jsonify, request
from routes.http_codes import http_okay, http_error_404
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
            "categories": [c.format() for c in categories],
            "currentCategory": categories[0].name
        })

    def get_by_category(category_id):
        category = Category.query.filter(Category.id == category_id).one()
        if category is not None:
            page = request.args.get("page", default=1, type=int)
            questions = Question.query.filter(Question.category.id == category_id)
            questions = questions.paginate(page, QUESTIONS_PER_PAGE, False).items
            questions = questions.order_by(Question.creation_date.asc())
            return http_okay({
                "questions": [q.format() for q in questions],
                "totalQuestions": len(questions),
                "currentCategory": category.name
            })
        else:
            return http_error_404()
