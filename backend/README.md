# TriviaApi/Backend

# Python, autopep8 and vscode
I use columnLimit = 120. You can copy paste that in your vscode settings if you want.
```
"python.linting.pylintArgs": [
    "--max-line-length=120"
],
"python.formatting.autopep8Args": [
    "--max-line-length=120"
]
```

# Setup postgresql
```bash
# sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
# sudo -u postgres psql -c "CREATE DATABASE testdb;"
# sudo -u postgres psql -c "ALTER DATABASE testdb SET TIMEZONE TO 'UTC';"
# sudo service postgresql start
```