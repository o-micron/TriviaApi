from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine, asc, desc
from models.shared import db, Operations


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False, unique=True)
    answer = Column(String, nullable=False)
    category = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)

    def __repr__(self):
        return f'''<
        Question id: {self.id},
        question: {self.question},
        answer: {self.answer},
        category: {self.category},
        difficulty: {self.difficulty}
        >'''

    def insert(self):
        Operations.insert(self)

    def update(self):
        Operations.update()

    def delete(self):
        Operations.delete(self)
