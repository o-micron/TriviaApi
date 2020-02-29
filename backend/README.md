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
psql postgres -c "CREATE DATABASE trivia;"
psql trivia -c "CREATE USER trivia_user WITH PASSWORD 'trivia_password'";
psql trivia -c "GRANT ALL PRIVILEGES ON DATABASE \"trivia\" to trivia_user";
```