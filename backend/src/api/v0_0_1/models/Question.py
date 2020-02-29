from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import ForeignKey, asc, desc
from models.shared import db, Operations

class Question(db.Model):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.now())
    question = Column(String, nullable=False, unique=True)
    answer = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    difficulty_id = Column(Integer, ForeignKey("difficulties.id"), nullable=False)

    def format(self):
        return {
            "id": self.id,
            "creation_date": self.creation_date.strftime("%Y-%m-%d %H-%M-%S"),
            "question": self.question,
            "answer": self.answer,
            "category": self.category.format(),
            "difficulty": self.difficulty.level
        }

    def insert(self):
        Operations.insert(self)

    def update(self):
        Operations.update()

    def delete(self):
        Operations.delete(self)

    def create_from_dict(d):
        question = d.get('question')
        answer = d.get('answer')
        category_id = d.get('category_id')
        difficulty_id = d.get('difficulty_id')
        return Question(creation_date=datetime.now(), question=question, answer=answer, category_id=category_id, difficulty_id=difficulty_id)
