from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from ClientModel import Client
from OrderModel import Order
import requests
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "rf;kpkvbdtjm;fpkdpvfjovjcdlnlpjvfl"
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

class Authorization(Resource):
    def login(self):
        data = requests.get_json(forse=True)
        #data = {'username': '', 'password': ''}
        info = Client.query.filter_by(username = data['username']).one_or_none()

        if data['password'] != info.password or info == None:
            return jsonify({"msg": "Bad password or username"}), 401
        access_token = create_access_token(identity=data['username'])
        return jsonify(access_token=access_token)

    @jwt_required()
    def logout(self):
        pass


class ClientApi(Resource):
    @staticmethod
    @jwt_required()
    def get(self, id=None):
        if id is None:
            info = Client.query.all()
            d = {}
            for i in info:
                d[i.id] = [i.username, i.password, i.f_name, i.l_name,]
            return d

        else:
            info = Client.query.get(id)
            return jsonify(id = info.id,
                           username = info.username,
                           password = info.password,
                           f_name = info.f_name,
                           l_name = info.l_name)

    @staticmethod
    def post(self):
        data = requests.get_json(forse=True)
        #data == {'f_name':..., ...}

        db.session.add(Client(username = data['username'],
                              password = data['password'],
                              f_name = data['f_name'],
                              l_name = data['l_name']))
        db.session.commit()
        return 200

    @staticmethod
    @jwt_required()
    def patch(self, id):
        data = requests.get_json(forse=True)
        # data == {'f_name':..., ...}
        Cl = Client.query.get(id)

        if data['username']:
            Cl.username = data['username']
        if data['password']:
            Cl.password = data['password']
        if data['f_name']:
            Cl.f_name = data['f_name']
        if data['l_name']:
            Cl.l_name = data['l_name']
        db.session.commit()
        return 200

    @staticmethod
    @jwt_required()
    def delete(self, id):
        c = Client.query.get(id)
        o = Order.query.filter(Order.client_id == id).all()
        db.session.delete(c)
        for i in o:
            db.session.delete(i)
        db.session.commit()
        return 200

class OrderApi(Resource):
    @staticmethod
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

    @staticmethod
    @jwt_required()
    def post(self):
        data = requests.get_json(forse=True)
        # data == {f_name:..., ...}

        db.session.add(Order(date = data['date'],
                            client_id = data['client_id'],
                            total = data['total']))
        db.session.commit()
        return 200

    @staticmethod
    @jwt_required()
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

    @staticmethod
    @jwt_required()
    def delete(self, id):
        o = Order.query.get(id)
        db.session.delete(o)
        db.session.commit()
        return 200

api.add_resource(Authorization, '/')
api.add_resource(ClientApi, '/client/', '/client/<int:id>')
api.add_resource(OrderApi, '/order/', '/order/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)