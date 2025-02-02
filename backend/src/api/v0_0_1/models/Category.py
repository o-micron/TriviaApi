from sqlalchemy import Column, String, Integer
from sqlalchemy import asc, desc
from models.shared import db, Operations


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    questions = db.relationship("Question", back_populates="category", lazy='subquery', cascade="all, delete-orphan")

    def format(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def insert(self):
        return Operations.insert(self)

    def update(self):
        return Operations.update()

    def delete(self):
        return Operations.delete(self)

    def create_from_dict(d):
        name = d.get('name')
        return Category(name=name)
