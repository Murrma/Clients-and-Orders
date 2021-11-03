from fastapi import FastAPI
from ClientModel import Client
from OrderModel import Order
from flask_sqlalchemy import SQLAlchemy

app = FastAPI()
db = SQLAlchemy(app)

@app.get("/client/items/{c_id}")
def get(c_id: int):
    if c_id is None:
        info = Client.query.all()
        d = {}
        for i in info:
            d[i.id] = [i.username, i.password, i.f_name, i.l_name, ]
        return d

    else:
        info = Client.query.get(c_id)
        return {'id': info.id,
                'username': info.username,
                'password': info.password,
                'f_name': info.f_name,
                'l_name': info.l_name}

@app.post('/client/create/')
def post(info: Client):
    db.session.add(Client(username=info['username'],
                          password=info['password'],
                          f_name=info['f_name'],
                          l_name=info['l_name']))
    db.session.commit()
    return 200

@app.patch('/client/change/{c_id}')
def patch(data: Client):
    Cl = Client.query.get(c_id)

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

@app.delete('/client/delete/{id}')
def delete():
    c = Client.query.get(id)
    o = Order.query.filter(Order.client_id == id).all()
    db.session.delete(c)
    for i in o:
        db.session.delete(i)
    db.session.commit()
    return 200
