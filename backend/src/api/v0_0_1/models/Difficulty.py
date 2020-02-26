from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine, asc, desc
from models.shared import db, Operations


class Difficulty(db.Model):
    __tablename__ = 'difficulties'

    name = Column(String, nullable=False, unique=True)
    index = Column(Integer, nullable=False, unique=True)

    def format(self):
        return {
            'name': {self.name},
            'index': {self.index}
        }

    def insert(self):
        Operations.insert(self)

    def update(self):
        Operations.update()

    def delete(self):
        Operations.delete(self)

    def get_by_index(index):
        try:
            difficulty = Difficulty.query.filter(Difficulty.index == index).one()
            return difficulty
        except Exception as ex:
            return None
