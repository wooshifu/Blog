from flask_sqlalchemy import SQLAlchemy

from .app import app

db = SQLAlchemy(app)

db_engine = db.engine
db_connection = db_engine.connect()
