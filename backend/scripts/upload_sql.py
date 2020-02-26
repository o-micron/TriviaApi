import json
import psycopg2
from datetime import datetime

# --------------------------------------------------------
# setup psycopg2, open connections etc ..
# --------------------------------------------------------
connection = psycopg2.connect("dbname='trivia' user='postgres' host='localhost' password='postgres'")
cursor = connection.cursor()
# --------------------------------------------------------

# --------------------------------------------------------
# upload data
# --------------------------------------------------------
categories = []
questions = []

with open('questions.json') as f:
    questions = json.load(f)

with open('categories.json') as f:
    categories = json.load(f)

print(questions)
print(categories)

difficulties = [q.get('difficulty') for q in questions]
difficulties = list(dict.fromkeys(difficulties))
difficulties.sort()

print(difficulties)

for d in difficulties:
    data = (d, d)
    try:
        cursor.execute("INSERT INTO difficulties (id, level) VALUES (%s, %s);", data)
        connection.commit()
    except psycopg2.IntegrityError as ex:
        connection.rollback()
        print("\n\n\n")
        print(ex)
        print("\n\n\n")

for c in categories:
    id = c.get('id')
    name = c.get('name')
    data = (id, name)
    try:
        cursor.execute("INSERT INTO categories (id, name) VALUES (%s, %s);", data)
        connection.commit()
    except psycopg2.IntegrityError as ex:
        connection.rollback()
        print("\n\n\n")
        print(ex)
        print("\n\n\n")


for q in questions:
    id = q.get('id')
    question = q.get('question')
    question = question.replace("'", "\'")
    answer = q.get('answer')
    answer = answer.replace("'", "\'")
    difficulty = q.get('difficulty')
    category = q.get('category')
    data = (id, datetime.now(), question, answer, difficulty, category)
    try:
        cursor.execute(
            "INSERT INTO questions (id, creation_date, question, answer, difficulty_id, category_id) VALUES (%s, %s, %s, %s, %s, %s);", data)
        connection.commit()
    except psycopg2.IntegrityError as ex:
        connection.rollback()
        print("\n\n\n")
        print(ex)
        print("\n\n\n")

# --------------------------------------------------------
