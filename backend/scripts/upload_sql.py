import json
import psycopg2

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
    cmd = "INSERT INTO difficulties (id, level) VALUES ({}, {});".format(d, d)
    try:
        cursor.execute(cmd)
        connection.commit()
    except psycopg2.IntegrityError:
        connection.rollback()

for c in categories:
    id = c.get('id')
    name = c.get('name')
    cmd = "INSERT INTO categories(id, name) VALUES({}, \"{}\");".format(id, name)
    try:
        cursor.execute(cmd)
        connection.commit()
    except psycopg2.IntegrityError:
        connection.rollback()


for q in questions:
    id = q.get('id')
    question = q.get('question')
    answer = q.get('answer')
    difficulty = q.get('difficulty')
    category = q.get('category')
    cmd = """
    INSERT INTO questions (id, question, answer, difficulty_id, category_id) VALUES ({}, {}, {}, {}, {});
    """.format(id, question, answer, difficulty, category)
    try:
        cursor.execute(cmd)
        connection.commit()
    except psycopg2.IntegrityError:
        connection.rollback()

# --------------------------------------------------------
