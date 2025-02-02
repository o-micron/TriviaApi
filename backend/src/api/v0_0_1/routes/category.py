import json
from flask import jsonify, request
from routes.http_codes import http_okay, http_created, http_error, http_error_400, http_error_404, http_not_modified, http_deleted
from models.shared import db
from models.Question import Question
from models.Category import Category
from models.Difficulty import Difficulty


class CategoryRouter:
    CATEGORIES_PER_PAGE = 5

    post_schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'}
        },
        'required': ['name']
    }
    patch_schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'}
        },
        'required': []
    }
    put_schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'}
        },
        'required': ['name']
    }

    def create(json_data):
        category = Category.create_from_dict(json_data)
        if category.insert():
            return http_created({"category": category.format()})
        return http_error_400()

    def modify_by_id(category_id, json_data):
        category = Category.query.filter(Category.id == category_id).first()
        if category is not None:
            category.name = json_data.get('name', category.name)
            if category.update():
                return http_okay({"category": category.format()})
            else:
                return http_not_modified()
        return http_error_404()

    def update_by_id(category_id, json_data):
        category = Category.query.filter(Category.id == category_id).first()
        if category is not None:
            category.name = json_data.get('name')
            if category.update():
                return http_okay({"category": category.format()})
            else:
                return http_not_modified()
        return http_error_404()

    def delete_by_id(category_id):
        category = Category.query.filter(Category.id == category_id).first()
        if category is not None:
            if category.delete():
                return http_deleted({"category": category.format()})
            return http_error(204, "no category found for the given id", {})
        return http_error_404()

    def get_all():
        categories = Category.query.order_by(Category.name.asc())
        return http_okay({
            "categories": [q.format() for q in categories.all()]
        })

    def get_paginated():
        page = request.args.get("page", default=1, type=int)
        categories = Category.query.order_by(Category.name.asc())
        total_categories = len(categories.all())
        categories = categories.paginate(page, CategoryRouter.CATEGORIES_PER_PAGE, False).items
        return http_okay({
            "categories": [q.format() for q in categories],
            "totalCategories": total_categories,
            "categoriesPerPage": CategoryRouter.CATEGORIES_PER_PAGE
        })

    def get_by_id(category_id):
        category = Category.query.filter(Category.id == category_id).first()
        if category is not None:
            return http_okay({"category": category.format()})
        return http_error_404()
