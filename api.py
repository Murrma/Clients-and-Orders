from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from ClientModel import Client
from OrderModel import Order
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


class ClientApi(Resource):
    def get(self, id=None):
        if id is None:
            info = Client.query.all()
            d = {}
            for i in info:
                d[i.id] = [i.f_name, i.l_name, i.gender]
            return d

        else:
            info = Client.query.get(id)
            return jsonify(id = info.id,
                           f_name = info.f_name,
                           l_name = info.l_name,
                           gender = info.gender)

    def post(self):
        data = requests.get_json(forse=True)
        #data == {f_name:..., ...}

        db.session.add(Client(f_name = data['f_name'],
                              l_name = data['l_name'],
                              gender = data['gender']))
        db.session.commit()
        return 200

    def patch(self, id):
        data = requests.get_json(forse=True)
        # data == {f_name:..., ...}
        Cl = Client.query.get(id)

        if data['f_name']:
            Cl.f_name = data['f_name']
        if data['l_name']:
            Cl.l_name = data['l_name']
        if data['gender']:
            Cl.gender = data['gender']
        db.session.commit()
        return 200

    def delete(self, id):
        c = Client.query.get(id)
        o = Order.query.filter(Order.client_id == id).all()
        db.session.delete(c)
        for i in o:
            db.session.delete(i)
        db.session.commit()
        return 200

class OrderApi(Resource):
    def get(self, id=None):
        if id is None:
            info = Order.query.all()
            d = {}
            for i in info:
                d[i.id] = [i.date, i.client_id, i.total]
            return d
        else:
            info = Order.query.get(id)
            return jsonify(id = info.id,
                           date = info.date,
                           client_id = info.client_id,
                           total = info.total)

    def post(self):
        data = requests.get_json(forse=True)
        # data == {f_name:..., ...}

        db.session.add(Order(date = data['date'],
                            client_id = data['client_id'],
                            total = data['total']))
        db.session.commit()
        return 200

    def patch(self, id):
        data = requests.get_json(forse=True)
        # data == {f_name:..., ...}
        Or = Order.query.get(id)

        if data['date']:
            Or.date = data['date']
        if data['client_id']:
            Or.client_id = data['client_id']
        if data['total']:
            Or.total = data['total']
        db.session.commit()
        return 200


    def delete(self, id):
        o = Order.query.get(id)
        db.session.delete(o)
        db.session.commit()
        return 200

api.add_resource(ClientApi, '/client/', '/client/<int:id>')
api.add_resource(OrderApi, '/order/', '/order/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
