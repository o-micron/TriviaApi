import os

# -----------------------------------------------------------------------------------------------
# Configurations
# -----------------------------------------------------------------------------------------------
DEBUG = True
DB_CONFIG = {
    'dialect': 'postgresql',
    'username': 'postgres',
    'password': 'postgres',
    'ip': 'localhost',
    'port': 5432,
    'name': 'trivia'
}
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# Connect to database
# -----------------------------------------------------------------------------------------------
try:
    with open('config.json') as f:
        DB_CONFIG = json.load(f)
except:
    print("Using the default db configuration")

DB_URL = '{dialect}://{username}:{password}@{ip}:{port}/{dbname}'.format(
    dialect=DB_CONFIG['dialect'],
    username=DB_CONFIG['username'],
    password=DB_CONFIG['password'],
    ip=DB_CONFIG['ip'],
    port=DB_CONFIG['port'],
    dbname=DB_CONFIG['name'])

SQLALCHEMY_DATABASE_URI = DB_URL
# -----------------------------------------------------------------------------------------------
