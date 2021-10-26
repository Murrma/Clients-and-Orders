from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Client(BaseModel):
    id: int
    username: str
    password: str
    f_name: str
    l_name: str
class Order(BaseModel):
    id = int
    date = str
    client_id = int
    total = str

@app.get("/client/items/{id}")
def get(id: int):
    if id is None:
        info = Client(id = id)
        d = {}
        for i in info:
            d[i.id] = [i.username, i.password, i.f_name, i.l_name, ]
        return d

    else:
        info = Client#
        return {'id': info.id,
                'username': info.username,
                'password': info.password,
                'f_name': info.f_name,
                'l_name': info.l_name}

@app.post('/client/create/')
def post(info: Client):
    return info

@app.patch('/client/change/{id}')
def patch():
    pass

@app.delete('/client/delete/{id}')
def delete():
    pass
