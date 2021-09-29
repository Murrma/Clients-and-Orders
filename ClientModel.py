from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), unique=True)
    l_name = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=True)

    def __init__(self, f_name, l_name, gender):
        self.f_name = f_name
        self.l_name = l_name
        self.gender = gender

    def __repr__(self):
        return f'id = {self.id}, name: {self.f_name}, surname: {self.l_name}, gender: {self.gender}'


db.create_all()
