from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Client(BaseModel):
    name: str
    is_offer: Optional[bool] = None

    id: Integer, primary_key=True)
    username: db.Column(db.String(50), unique=True)
    password: db.Column(db.String(100), unique=True)
    f_name: db.Column(db.String(50), unique=True)
    l_name: str

@app.get("/client/items/{id}")
def get(id: int):
    if id is None:
        info = Client.query.all()
        d = {}
        for i in info:
            d[i.id] = [i.username, i.password, i.f_name, i.l_name, ]
        return d

    else:
        info = Client.query.get(id)
        return {'id': info.id,
                'username': info.username,
                'password': info.password,
                'f_name': info.f_name,
                'l_name': info.l_name}

@app.post('/client/create/')
def post():


@app.patch('/client/change/{id}')
def patch():
    pass

@app.delete('/client/delete/{id}')
def delete():
    pass