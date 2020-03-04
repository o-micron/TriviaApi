from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Operations:
    def rollback():
        db.session.rollback()

    def insert(model):
        try:
            db.session.add(model)
            db.session.commit()
            return True
        except Exception as ex:
            Operations.rollback()
            print(ex)
            return False

    def update():
        try:
            db.session.commit()
            return True
        except Exception as ex:
            Operations.rollback()
            print(ex)
            return False

    def delete(model):
        try:
            db.session.delete(model)
            db.session.commit()
            return True
        except Exception as ex:
            Operations.rollback()
            print(ex)
            return False


class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
