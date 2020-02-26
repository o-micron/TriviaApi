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
# for q in questions:
#     id = q.get('id')
#     question = q.get('question')
#     answer = q.get('answer')
#     difficulty = q.get('difficulty')
#     category = q.get('category')
# --------------------------------------------------------
