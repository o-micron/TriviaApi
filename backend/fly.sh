VERSION=v0_0_1
cd src/api/$VERSION
export FLASK_APP=app.py
export FLASK_DEBUG=true
flask run