from sqlalchemy import Column, String, Integer
from sqlalchemy import asc, desc
from models.shared import db, Operations


class Difficulty(db.Model):
    __tablename__ = "difficulties"

    id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False, unique=True)
    questions = db.relationship("Question", back_populates="difficulty", lazy='subquery')

    def format(self):
        return {
            "id": self.id,
            "level": self.level
        }

    def insert(self):
        return Operations.insert(self)

    def update(self):
        return Operations.update()

    def delete(self):
        return Operations.delete(self)
