import json
from flask import jsonify, request
from routes.http_codes import http_okay, http_created, http_deleted, http_error, http_error_400, http_error_404
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty

QUESTIONS_PER_PAGE = 5


class QuestionRouter:
    schema = {
        'type': 'object',
        'properties': {
            'question': {'type': 'string'},
            'answer': {'type': 'string'},
            'category_id': {'type': 'number'},
            'difficulty_id': {'type': 'number'}
        },
        'required': ['question', 'answer', 'category_id', 'difficulty_id']
    }

    def create(json_data):
        print(json_data)
        question = Question.create_from_dict(json_data)
        if question.insert():
            return http_created({ "data": question.format() })
        return http_error_400()

    def delete(question_id):
        question = Question.query.filter(Question.id == question_id).first()
        if question is not None:
            if question.delete():
                return http_deleted({ "data": question.format() })
            return http_error(204, "no question found for the given id", {})
        return http_error_400()

    def get_details(question_id):
        question = Question.query.filter(Question.id == question_id).first()
        if question is not None:
            return http_okay({ "data": question.format() })
        return http_error_400()

    def get_all():
        page = request.args.get("page", default=1, type=int)
        questions = Question.query.order_by(Question.creation_date.asc())
        totalQuestions = len(questions.all())
        questions = questions.paginate(page, QUESTIONS_PER_PAGE, False).items
        categories = Category.query.order_by(Category.name.asc())
        return http_okay({
            "questions": [q.format() for q in questions],
            "totalQuestions": totalQuestions,
            "questionsPerPage": QUESTIONS_PER_PAGE,
            "categories": [c.format() for c in categories],
            "currentCategory": categories[0].name
        })

    def get_by_category(category_id):
        category = Category.query.filter(Category.id == category_id).first()
        if category is not None:
            page = request.args.get("page", default=1, type=int)
            questions = Question.query.filter(Question.category_id == category_id)
            questions = questions.order_by(Question.creation_date.asc())
            totalQuestions = len(questions.all())
            questions = questions.paginate(page, QUESTIONS_PER_PAGE, False).items
            return http_okay({
                "questions": [q.format() for q in questions],
                "totalQuestions": totalQuestions,
                "questionsPerPage": QUESTIONS_PER_PAGE,
                "currentCategory": category.name
            })
        else:
            return http_error_404()

    def get_by_difficulty(difficulty_id):
        difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).first()
        if difficulty is not None:
            page = request.args.get("page", default=1, type=int)
            questions = Question.query.filter(Question.difficulty_id == difficulty_id)
            questions = questions.order_by(Question.creation_date.asc())
            totalQuestions = len(questions.all())
            questions = questions.paginate(page, QUESTIONS_PER_PAGE, False).items
            return http_okay({
                "questions": [q.format() for q in questions],
                "totalQuestions": totalQuestions,
                "questionsPerPage": QUESTIONS_PER_PAGE,
                "currentDifficulty": difficulty.level
            })
        else:
            return http_error_404()
