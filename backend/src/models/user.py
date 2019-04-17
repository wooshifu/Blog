from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f'<User {self.username}, {self.email}>'
