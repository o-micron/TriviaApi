import json
from flask import jsonify
from routes.http_codes import http_okay
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty


class DifficultyRouter:
    def get_all():
        difficulties = Difficulty.query.order_by(Difficulty.level.asc()).all()
        return http_okay({
            "data": [q.format() for q in difficulties]
        })
