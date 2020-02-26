# sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
# psql trivia < trivia.psql
# sudo service postgresql start
import json
import psycopg2

# --------------------------------------------------------
# setup psycopg2, open connections etc ..
# --------------------------------------------------------
connection = psycopg2.connect("dbname='trivia' user='postgres' host='localhost' password='postgres'")
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
cursor.execute("DROP TABLE questions;")
connection.commit()

cursor.execute("SELECT * FROM categories;")
connection.commit()
categories = [{
    "id": category[0],
    "name": category[1]
} for category in cursor.fetchall()]
cursor.execute("DROP TABLE categories;")
connection.commit()
# --------------------------------------------------------

# --------------------------------------------------------
# export to json
# --------------------------------------------------------
questions.sort(key=lambda x: x['id'], reverse=True)
categories.sort(key=lambda x: x['id'], reverse=True)

with open('questions.json', 'w') as f:
    json.dump(questions, f)

with open('categories.json', 'w') as f:
    json.dump(categories, f)
# --------------------------------------------------------


# --------------------------------------------------------
# cleanup ..
# --------------------------------------------------------
cursor.close()
connection.close()
# --------------------------------------------------------
