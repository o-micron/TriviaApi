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
            'category_id': {'type': 'number'},
            'difficulty_id': {'type': 'number'},
            'previous_questions': {'type': 'array'}
        },
        'required': ['category_id', 'difficulty_id', 'previous_questions']
    }

    def get_next_question(json_data):
        category_id = json_data.get('category_id')
        difficulty_id = json_data.get('difficulty_id')
        previous_questions = json_data.get('previous_questions')
        category = Category.query.filter(Category.id == category_id).first()
        difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).first()
        if category is not None:
            if difficulty is not None:
                previous_questions = [pq.get('id') for pq in previous_questions]
                f = (Question.category_id == category_id and Question.difficulty_id == difficulty_id)
                questions = Question.query.filter(f).order_by(Question.creation_date.asc()).all()
                total_questions = len(questions)
                remaining_questions = total_questions - len(previous_questions) - 1
                questions = list(filter(lambda q: q.id not in previous_questions, questions))
                random.shuffle(questions)
                if len(questions) > 0:
                    return http_okay({
                        "question": questions[0].format(),
                        "remaining_questions": remaining_questions,
                        "total_questions": total_questions
                    })
                return http_error_404({"hint": "no question left available for the given difficulty and category"})
            return http_error_404({"hint": "no difficulty available with the given difficulty id"})
        return http_error_404({"hint": "no difficulty available with the given difficulty id"})
