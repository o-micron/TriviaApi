import json
from flask import jsonify, request
from routes.http_codes import http_okay
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty

CATEGORIES_PER_PAGE = 5


class CategoryRouter:
    def get_all():
        page = request.args.get("page", default=1, type=int)
        categories = Category.query.order_by(Category.name.asc())
        total_categories = len(categories.all())
        categories = categories.paginate(page, CATEGORIES_PER_PAGE, False).items
        return http_okay({
            "categories": [q.format() for q in categories],
            "totalCategories": total_categories,
            "categoriesPerPage": CATEGORIES_PER_PAGE
        })
