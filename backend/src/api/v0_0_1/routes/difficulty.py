import json
from flask import jsonify, request
from routes.http_codes import http_okay, http_created, http_error, http_error_400, http_error_404, http_not_modified, http_deleted
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty


class DifficultyRouter:
    DIFFICULTIES_PER_PAGE = 5

    post_schema = {
        'type': 'object',
        'properties': {
            'level': {'type': 'number'}
        },
        'required': ['level']
    }
    patch_schema = {
        'type': 'object',
        'properties': {
            'level': {'type': 'number'}
        },
        'required': []
    }
    put_schema = {
        'type': 'object',
        'properties': {
            'level': {'type': 'number'}
        },
        'required': ['level']
    }

    def create(json_data):
        difficulty = Difficulty.create_from_dict(json_data)
        if difficulty.insert():
            return http_created({"difficulty": difficulty.format()})
        return http_error_400()

    def modify_by_id(difficulty_id, json_data):
        difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).first()
        if difficulty is not None:
            difficulty.level = json_data.get('level', difficulty.level)
            if difficulty.update():
                return http_okay({"difficulty": difficulty.format()})
            else:
                return http_not_modified()
        return http_error_404()

    def update_by_id(difficulty_id, json_data):
        difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).first()
        if difficulty is not None:
            difficulty.level = json_data.get('level')
            if difficulty.update():
                return http_okay({"difficulty": difficulty.format()})
            else:
                return http_not_modified()
        return http_error_404()

    def delete_by_id(difficulty_id):
        difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).first()
        if difficulty is not None:
            if difficulty.delete():
                return http_deleted({"difficulty": difficulty.format()})
            return http_error(204, "no difficulty found for the given id")
        return http_error_404()

    def get_all():
        difficulties = Difficulty.query.order_by(Difficulty.level.asc())
        return http_okay({
            "difficulties": [q.format() for q in difficulties.all()]
        })

    def get_paginated():
        page = request.args.get("page", default=1, type=int)
        difficulties = Difficulty.query.order_by(Difficulty.level.asc())
        total_difficulties = len(difficulties.all())
        difficulties = difficulties.paginate(page, DifficultyRouter.DIFFICULTIES_PER_PAGE, False).items
        return http_okay({
            "difficulties": [q.format() for q in difficulties],
            "totalDifficulties": total_difficulties,
            "difficultiesPerPage": DifficultyRouter.DIFFICULTIES_PER_PAGE
        })

    def get_by_id(difficulty_id):
        difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).first()
        if difficulty is not None:
            return http_okay({"difficulty": difficulty.format()})
        return http_error_404()
