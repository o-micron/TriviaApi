import json
from flask import jsonify, request
from routes.http_codes import http_okay, http_created, http_not_modified, http_deleted, http_error, http_error_400, http_error_404
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty

QUESTIONS_PER_PAGE = 5


class QuestionRouter:
    post_schema = {
        'type': 'object',
        'properties': {
            'question': {'type': 'string'},
            'answer': {'type': 'string'},
            'category_id': {'type': 'number'},
            'difficulty_id': {'type': 'number'}
        },
        'required': ['question', 'answer', 'category_id', 'difficulty_id']
    }
    patch_schema = {
        'type': 'object',
        'properties': {
            'question': {'type': 'string'},
            'answer': {'type': 'string'},
                'category_id': {'type': 'number'},
                'difficulty_id': {'type': 'number'}
        },
        'required': []
    }
    put_schema = {
        'type': 'object',
        'properties': {
            'question': {'type': 'string'},
            'answer': {'type': 'string'},
            'category_id': {'type': 'number'},
            'difficulty_id': {'type': 'number'}
        },
        'required': ['question', 'answer', 'category_id', 'difficulty_id']
    }
    search_schema = {
        'type': 'object',
        'properties': {
            'query': {'type': 'string'},
            'category_id': {'type': 'number'},
        },
        'required': ['query']
    }

    def create(json_data):
        print(json_data)
        question = Question.create_from_dict(json_data)
        if question.insert():
            return http_created({"data": question.format()})
        return http_error_400()

    def modify(question_id, json_data):
        question = Question.query.filter(Question.id == question_id).first()
        if question is not None:
            question.question = json_data.get('question', question.question)
            question.answer = json_data.get('answer', question.answer)
            question.category_id = json_data.get('category_id', question.category_id)
            question.difficulty_id = json_data.get('difficulty_id', question.difficulty_id)
            if question.update():
                return http_okay({"data": question.format()})
            else:
                return http_not_modified()
        return http_error_404()

    def update(question_id, json_data):
        question = Question.query.filter(Question.id == question_id).first()
        if question is not None:
            question.question = json_data.get('question')
            question.answer = json_data.get('answer')
            question.category_id = json_data.get('category_id')
            question.difficulty_id = json_data.get('difficulty_id')
            if question.update():
                return http_okay({"data": question.format()})
            else:
                return http_not_modified()
        return http_error_404()

    def delete(question_id):
        question = Question.query.filter(Question.id == question_id).first()
        if question is not None:
            if question.delete():
                return http_deleted({"data": question.format()})
            return http_error(204, "no question found for the given id", {})
        return http_error_404()

    def search(json_data):
        page = request.args.get("page", default=1, type=int)
        query = json_data.get('query').lower()
        category_id = json_data.get('category_id', -1)
        questions = Question.query.filter(Question.question.ilike('%' + query + '%'))
        if category_id > 0:
            questions = questions.filter(Question.category_id == category_id)
        questions = questions.order_by(Question.creation_date.asc())
        total_questions = len(questions.all())
        questions = questions.paginate(page, QUESTIONS_PER_PAGE, False).items
        return http_okay({
            "questions": [q.format() for q in questions],
            "total_questions": total_questions,
            "currentCategory": questions[0].category.name if len(questions) > 0 else None
        })

    def get_details(question_id):
        question = Question.query.filter(Question.id == question_id).first()
        if question is not None:
            return http_okay({"data": question.format()})
        return http_error_404()

    def get_all():
        page = request.args.get("page", default=1, type=int)
        questions = Question.query.order_by(Question.creation_date.asc())
        total_questions = len(questions.all())
        questions = questions.paginate(page, QUESTIONS_PER_PAGE, False).items
        categories = Category.query.order_by(Category.name.asc())
        return http_okay({
            "questions": [q.format() for q in questions],
            "totalQuestions": total_questions,
            "questionsPerPage": QUESTIONS_PER_PAGE,
            "categories": [c.format() for c in categories],
            "currentCategory": questions[0].category.name if len(questions) > 0 else None
        })

    def get_by_category(category_id):
        category = Category.query.filter(Category.id == category_id).first()
        if category is not None:
            page = request.args.get("page", default=1, type=int)
            questions = Question.query.filter(Question.category_id == category_id)
            questions = questions.order_by(Question.creation_date.asc())
            total_questions = len(questions.all())
            questions = questions.paginate(page, QUESTIONS_PER_PAGE, False).items
            return http_okay({
                "questions": [q.format() for q in questions],
                "totalQuestions": total_questions,
                "questionsPerPage": QUESTIONS_PER_PAGE,
                "currentCategory": category.name
            })
        else:
            return http_error_404()

    def get_by_difficulty(difficulty_id):
        difficulty = Difficulty.query.filter(
            Difficulty.id == difficulty_id).first()
        if difficulty is not None:
            page = request.args.get("page", default=1, type=int)
            questions = Question.query.filter(Question.difficulty_id == difficulty_id)
            questions = questions.order_by(Question.creation_date.asc())
            total_questions = len(questions.all())
            questions = questions.paginate(page, QUESTIONS_PER_PAGE, False).items
            return http_okay({
                "questions": [q.format() for q in questions],
                "totalQuestions": total_questions,
                "questionsPerPage": QUESTIONS_PER_PAGE,
                "currentDifficulty": difficulty.level
            })
        else:
            return http_error_404()
