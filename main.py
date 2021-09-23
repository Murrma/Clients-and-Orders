from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Clients(db.Model):
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

    def get(id = None):
        try:
            if id == None:
                info = Clients.query.all()
            else:
                info = Clients.query.get(id)
        except:
            info = "Ошибка чтения из БД"

        return info

    def post(self):
        data = request.get_json(force = True)
        #{'f_name': 'Ann', 'l_name': 'efae', 'gender': 'acacffgh'}
        nc = Clients(f_name = data['f_name'],
                     l_name = data['l_name'],
                     gender = data['gender'])
        db.session.add(nc)
        db.session.commit()
        return 'done'

    def patch(self):
        pass

    def delete(self):
        pass



'''
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=True)
    client_id = db.Column(db.Integer)
    total = db.Column(db.String(100))

    def __repr__(self):
        return f"id = {self.id}, date: {self.date}, owner: {self.client_id}, total: {self.total}"
'''

db.create_all()