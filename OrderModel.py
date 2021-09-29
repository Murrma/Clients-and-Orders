from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=True)
    client_id = db.Column(db.Integer, nullable=True)
    total = db.Column(db.String(10), nullable=True)

    def __init__(self, date, client_id, total):
        self.date = date
        self.client_id = client_id
        self.total = total

    def __repr__(self):
        return f"id = {self.id}, date: {self.date}, owner: {self.client_id}, total: {self.total}"

db.create_all()