rm -rf migrations/
rm -rf scripts/*.json
cd data
sudo -u postgres psql -c "DROP DATABASE trivia;"
sudo -u postgres psql -c "CREATE DATABASE trivia;"
psql trivia < trivia.psql
cd ../scripts
python3 load_sql.py
VERSION=v0_0_1
cd ../src/api/$VERSION
export FLASK_APP=app.py
export FLASK_DEBUG=true
flask db init
flask db migrate
flask db upgrade
cd ../../../scripts
python3 upload_sql.py