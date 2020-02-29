rm -rf scripts/*.json
cd data
psql postgres -c "DROP DATABASE trivia;"
psql postgres -c "CREATE DATABASE trivia;"
psql -d trivia -U trivia_user -f trivia.psql
cd ../scripts
python3 load_sql.py
psql postgres -c "DROP DATABASE trivia;"
psql postgres -c "CREATE DATABASE trivia;"
VERSION=v0_0_1
cd ../src/api/$VERSION
rm -rf migrations/
export FLASK_APP=app.py
export FLASK_DEBUG=true
flask db init
flask db migrate
flask db upgrade
cd ../../../scripts
python3 upload_sql.py