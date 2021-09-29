from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from ClientModel import Client
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


class ClientApi(Resource):
    def get(self, id=None):
        if id == None:
            info = Client.query.all()
            return #info in json

        else:
            info = Client.query.get(id)
            return jsonify(id = info.id,
                           f_name = info.f_name,
                           l_name = info.l_name,
                           gender = info.gender)

    def post(self):
        data = requests.get_json(forse=True)
        #data == {id:..., f_name:..., ...}




api.add_resource(ClientApi, '/', '/<int:id>')
# api.add_resource()

if __name__ == '__main__':
    app.run(debug=True)