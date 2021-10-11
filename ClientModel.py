from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100), unique=True)
    f_name = db.Column(db.String(50), unique=True)
    l_name = db.Column(db.String(50), nullable=True)

    def __init__(self, username, password, f_name, l_name):
        self.username = username
        self.password = password
        self.f_name = f_name
        self.l_name = l_name


    def __repr__(self):
        return f'id = {self.id}, username: {self.username}, password: {self.password}, name: {self.f_name}, surname: {self.l_name}'


db.create_all()
