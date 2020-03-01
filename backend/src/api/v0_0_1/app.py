import os
from flask import Flask, jsonify, request, g
from flask_migrate import Migrate
from flask_expects_json import expects_json
from routes.http_codes import http_okay, http_error_500, http_error_405, http_error_404, http_error_401, http_error_400

from models.shared import db
from routes.question import QuestionRouter
from routes.category import CategoryRouter
from routes.difficulty import DifficultyRouter

# -----------------------------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object('config')
app.config['JSON_AS_ASCII'] = False
db.init_app(app)

migrate = ''
with app.app_context():
    migrate = Migrate(app, db)
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------------------------
API_VERSION = os.path.basename(os.path.dirname(__file__))  # in example, v0_0_1


def route_by_version(rule, **options):
    def decorator(f):
        endpoint = options.pop("endpoint", None)
        app.add_url_rule("/api/{}{}".format(API_VERSION, rule), endpoint, f, **options)
        return f
    return decorator
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# Errors
# -----------------------------------------------------------------------------------------------
@app.errorhandler(500)
def server_error_500(error):
    return http_error_500()


@app.errorhandler(405)
def server_error_405(error):
    return http_error_405()


@app.errorhandler(404)
def server_error_404(error):
    return http_error_404()


@app.errorhandler(401)
def server_error_401(error):
    return http_error_401()


@app.errorhandler(400)
def server_error_400(error):
    return http_error_400()

# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------------------------
# Create a new question
@route_by_version('/questions', methods=['POST'])
@expects_json(QuestionRouter.schema)
def create_question():
    return QuestionRouter.create(g.data)

# Get all available questions, paginated
@route_by_version('/questions', methods=['GET'])
def all_questions():
    return QuestionRouter.get_all()

# Get a question by id
@route_by_version('/questions/<int:question_id>', methods=['GET', 'DELETE'])
def get_question_by_id(question_id):
    if request.method == 'GET':
        return QuestionRouter.get_details(question_id)
    if request.method == 'DELETE':
        return QuestionRouter.delete(question_id)


# Get all available categories, paginated
@route_by_version('/categories', methods=['GET'])
def all_categories():
    return CategoryRouter.get_all()

# Get questions by a specific category
@route_by_version('/categories/<int:category_id>/questions', methods=['GET'])
def get_questions_by_category(category_id):
    return QuestionRouter.get_by_category(category_id)

# Get all available difficulties, paginated
@route_by_version('/difficulties', methods=['GET'])
def all_difficulties():
    return DifficultyRouter.get_all()

# Get questions by a specific difficulty
@route_by_version('/difficulties/<int:difficulty_id>/questions', methods=['GET'])
def get_questions_by_difficulty(difficulty_id):
    return QuestionRouter.get_by_difficulty(difficulty_id)
# -----------------------------------------------------------------------------------------------
