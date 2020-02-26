from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine, asc, desc
from models.shared import db, Operations


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)

    def format(self):
        return {
            'id': {self.id},
            'type': {self.type}
        }

    def insert(self):
        Operations.insert(self)

    def update(self):
        Operations.update()

    def delete(self):
        Operations.delete(self)

    def get_by_id(id):
        try:
            category = Category.query.filter(Category.id == id).one()
            return category
        except Exception as ex:
            return None
