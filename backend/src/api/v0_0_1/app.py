from flask import Flask, jsonify, request
from flask_migrate import Migrate
from routes.http_codes import http_okay, http_error_500, http_error_405, http_error_404, http_error_401, http_error_400

from models.shared import db
from routes.question import QuestionRouter
# -----------------------------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

migrate = ''
with app.app_context():
    migrate = Migrate(app, db)
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
# Home
# -----------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return http_okay({
        "data": "hello world"
    })
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# Question
# -----------------------------------------------------------------------------------------------
@app.route('/api/v0_0_1/questions', methods=['GET', 'POST'])
def all_questions():
    if request.method == 'GET':
        return QuestionRouter.get_all()
    else:
        return http_error_404()
# -----------------------------------------------------------------------------------------------
