import json
from flask import jsonify
from routes.http_codes import http_okay
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty


class CategoryRouter:
    def get_all():
        categories = Category.query.order_by(Category.name.asc()).all()
        return http_okay({
            "data": [q.format() for q in categories]
        })
