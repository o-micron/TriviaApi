import json
from flask import jsonify, request
from routes.http_codes import http_okay
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty

DIFFICULTIES_PER_PAGE = 5


class DifficultyRouter:
    def get_all():
        page = request.args.get("page", default=1, type=int)
        difficulties = Difficulty.query.order_by(Difficulty.level.asc())
        total_difficulties = len(difficulties.all())
        difficulties = difficulties.paginate(page, DIFFICULTIES_PER_PAGE, False).items
        return http_okay({
            "difficulties": [q.format() for q in difficulties],
            "totalDifficulties": total_difficulties,
            "difficultiesPerPage": DIFFICULTIES_PER_PAGE
        })
