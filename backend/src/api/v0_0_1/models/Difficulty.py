from sqlalchemy import Column, String, Integer
from sqlalchemy import asc, desc
from models.shared import db, Operations


class Difficulty(db.Model):
    __tablename__ = "difficulties"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    questions = db.relationship("Question", backref="difficulty")

    def format(self):
        return {
            "id": {self.id},
            "name": {self.name}
        }

    def insert(self):
        Operations.insert(self)

    def update(self):
        Operations.update()

    def delete(self):
        Operations.delete(self)
