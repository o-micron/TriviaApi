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
            return False

    def update():
        try:
            db.session.commit()
            return True
        except Exception as ex:
            Operations.rollback()
            return False

    def delete(model):
        try:
            db.session.delete(model)
            db.session.commit()
            return True
        except Exception as ex:
            Operations.rollback()
            return False
