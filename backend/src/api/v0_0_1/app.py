import os
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from flask_migrate import Migrate
from flask_expects_json import expects_json
from routes.http_codes import http_okay, http_error_500, http_error_405, http_error_404, http_error_401, http_error_400

from models.shared import db
from routes.question import QuestionRouter
from routes.category import CategoryRouter
from routes.difficulty import DifficultyRouter
from routes.quiz import QuizRouter

# -----------------------------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------------------------
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
db.init_app(app)

migrate = ''
with app.app_context():
    migrate = Migrate(app, db)
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------------------------
# tie the folder name with the version of the api
API_VERSION = os.path.basename(os.path.dirname(__file__))  # in example, v0_0_1


def route_by_version(rule, **options):
    """
        This is created to ensure that if we take the same code and we simply change the name
        of the folder to vX.Y.Z we will automatically have routes starting with
        /api/<version>/<the actual endpoint>

        which means we can easily change the version of the code without lots of changes to
        the core implementation .. may be helpful sometime in the future 🤠 
    """
    def decorator(f):
        endpoint = options.pop("endpoint", None)
        app.add_url_rule("/api/{}{}".format(API_VERSION, rule), endpoint, f, **options)
        return f
    return decorator


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,True')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,PUT,POST,DELETE')
    return response
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
# /categories
# -----------------------------------------------------------------------------------------------
@route_by_version('/categories', methods=['POST'])
@expects_json(CategoryRouter.post_schema)
def create_category():
    return CategoryRouter.create(g.data)

# Get all available categories, paginated
@route_by_version('/categories', methods=['GET'])
def all_categories():
    return CategoryRouter.get_all()

# Partially modify a category by id
@route_by_version('/categories/<int:category_id>', methods=['PATCH'])
@expects_json(CategoryRouter.patch_schema)
def modify_category_by_id(category_id):
    return CategoryRouter.modify(category_id, g.data)

# Update a category by id
@route_by_version('/categories/<int:category_id>', methods=['PUT'])
@expects_json(CategoryRouter.put_schema)
def update_category_by_id(category_id):
    return CategoryRouter.update(category_id, g.data)

# Delete a category by id
@route_by_version('/categories/<int:category_id>', methods=['DELETE'])
def delete_category_by_id(category_id):
    return CategoryRouter.delete(category_id)

# Get questions by a specific category
@route_by_version('/categories/<int:category_id>/questions', methods=['GET'])
def get_questions_by_category(category_id):
    return QuestionRouter.get_by_category(category_id)
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# /difficulties
# -----------------------------------------------------------------------------------------------
@route_by_version('/difficulties', methods=['POST'])
@expects_json(DifficultyRouter.post_schema)
def create_difficulty():
    return DifficultyRouter.create(g.data)

# Get all available difficulties, paginated
@route_by_version('/difficulties', methods=['GET'])
def all_difficulties():
    return DifficultyRouter.get_all()

# Partially modify a difficulty by id
@route_by_version('/difficulties/<int:difficulty_id>', methods=['PATCH'])
@expects_json(DifficultyRouter.patch_schema)
def modify_difficulty_by_id(difficulty_id):
    return DifficultyRouter.modify(difficulty_id, g.data)

# Update a difficulty by id
@route_by_version('/difficulties/<int:difficulty_id>', methods=['PUT'])
@expects_json(DifficultyRouter.put_schema)
def update_difficulty_by_id(difficulty_id):
    return DifficultyRouter.update(difficulty_id, g.data)

# Delete a difficulty by id
@route_by_version('/difficulties/<int:difficulty_id>', methods=['DELETE'])
def delete_difficulty_by_id(difficulty_id):
    return DifficultyRouter.delete(difficulty_id)

# Get questions by a specific difficulty
@route_by_version('/difficulties/<int:difficulty_id>/questions', methods=['GET'])
def get_questions_by_difficulty(difficulty_id):
    return QuestionRouter.get_by_difficulty(difficulty_id)
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# /questions
# -----------------------------------------------------------------------------------------------
# Create a new question
@route_by_version('/questions', methods=['POST'])
@expects_json(QuestionRouter.post_schema)
def create_question():
    return QuestionRouter.create(g.data)

# search for a question
@route_by_version('/questions/search', methods=['POST'])
@expects_json(QuestionRouter.search_schema)
def search_for_question():
    return QuestionRouter.search(g.data)

# Get all available questions, paginated
@route_by_version('/questions', methods=['GET'])
def all_questions():
    return QuestionRouter.get_all()

# Get a question by id
@route_by_version('/questions/<int:question_id>', methods=['GET'])
def get_question_by_id(question_id):
    return QuestionRouter.get_details(question_id)

# Partially modify a question by id
@route_by_version('/questions/<int:question_id>', methods=['PATCH'])
@expects_json(QuestionRouter.patch_schema)
def modify_question_by_id(question_id):
    return QuestionRouter.modify(question_id, g.data)

# Update a question by id
@route_by_version('/questions/<int:question_id>', methods=['PUT'])
@expects_json(QuestionRouter.put_schema)
def update_question_by_id(question_id):
    return QuestionRouter.update(question_id, g.data)

# Delete a question by id
@route_by_version('/questions/<int:question_id>', methods=['DELETE'])
def delete_question_by_id(question_id):
    return QuestionRouter.delete(question_id)
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# /quizzes
# -----------------------------------------------------------------------------------------------
@route_by_version('/quizzes', methods=['POST'])
@expects_json(QuizRouter.next_question_schema)
def get_next_quiz_question():
    return QuizRouter.get_next_question(g.data)
# -----------------------------------------------------------------------------------------------
