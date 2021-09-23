from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
import json
from main import Clients, Orders

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class ClientApi(Resource):
    def get(self):
        qq = Clients.get()
        return jsonify(qq)

    def post(self):
        qq = Clients.post()
        return jsonify(qq)





api.add_resource(ClientApi, '/')
#api.add_resource()



if __name__ == '__main__':
    app.run(debug=True)
'''
1 Прописать в классах функционал и init
2 АПИ содержит вызовы функционала 1
3 
'''