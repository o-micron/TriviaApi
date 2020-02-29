# psql postgres -c "CREATE DATABASE trivia;"
# psql postgres -c "CREATE USER trivia_user WITH PASSWORD 'trivia_password'";
# psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE \"trivia\" to trivia_user";
import json
import psycopg2

# --------------------------------------------------------
# setup psycopg2, open connections etc ..
# --------------------------------------------------------
connection = psycopg2.connect("dbname='trivia' user='trivia_user' host='localhost' password='trivia_password'")
cursor = connection.cursor()
# --------------------------------------------------------

# --------------------------------------------------------
# get all data from the sql file then drop the tables
# --------------------------------------------------------
cursor.execute("SELECT * FROM questions;")
connection.commit()
questions = [{
    "id": question[0],
    "question": question[1],
    "answer": question[2],
    "difficulty": question[3],
    "category": question[4]
} for question in cursor.fetchall()]

cursor.execute("SELECT * FROM categories;")
connection.commit()
categories = [{
    "id": category[0],
    "name": category[1]
} for category in cursor.fetchall()]
# --------------------------------------------------------

# --------------------------------------------------------
# export to json
# --------------------------------------------------------
questions.sort(key=lambda x: x['id'])
categories.sort(key=lambda x: x['id'])

with open('questions.json', 'w') as f:
    json.dump(questions, f, ensure_ascii=False)

with open('categories.json', 'w') as f:
    json.dump(categories, f, ensure_ascii=False)
# --------------------------------------------------------


# --------------------------------------------------------
# cleanup ..
# --------------------------------------------------------
cursor.close()
connection.close()
# --------------------------------------------------------
