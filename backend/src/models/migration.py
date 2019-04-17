from sqlalchemy import func

from app import db


class Migration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    migration = db.Column(db.String, nullable=False, unique=True)
    sql = db.Column(db.String, nullable=True, unique=False)
    parameter = db.Column(db.String, nullable=True, unique=False)
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String, nullable=True, unique=False)

    def __repr__(self):
        return f'<Migration id: {self.id}, migration: {self.migration}, sql: {self.sql}>'
