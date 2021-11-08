from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///fast.db', echo=True)
Base = declarative_base()

class Client(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")

async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/client/items/{c_id}")
def get(c_id: int, current_user: User = Depends(get_current_active_user)):
    if c_id is None:
        info = Client.query.all()
        d = {}
        for i in info:
            d[i.id] = [i.username, i.password, i.f_name, i.l_name]
        return d

    else:
        info = Client.query.get(c_id)
        return {'id': info.id,
                'username': info.username,
                'password': info.password,
                'f_name': info.f_name,
                'l_name': info.l_name}

@app.post('/client/create/')
def post(info: Client, current_user: User = Depends(get_current_active_user)):
    db.session.add(Client(username=info['username'],
                          password=info['password'],
                          f_name=info['f_name'],
                          l_name=info['l_name']))
    db.session.commit()
    return 200

@app.patch('/client/change/{c_id}')
def patch(data: Client, current_user: User = Depends(get_current_active_user)):
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
def delete(current_user: User = Depends(get_current_active_user)):
    c = Client.query.get(id)
    o = Order.query.filter(Order.client_id == id).all()
    db.session.delete(c)
    for i in o:
        db.session.delete(i)
    db.session.commit()
    return 200
