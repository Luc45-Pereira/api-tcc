from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import dotenv
import src.Connection.conn as conn
import src.Objetos.User as User

dotenv.load_dotenv()

conection = conn.Conn()

app = FastAPI()


class Users(BaseModel):
    name: str
    email: str
    password: str
    type: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users")
def read_users():
    user = User.User(conection, 1)
    return user.buscar_todos()

@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = User.User(conection)
    user.buscar(user_id)
    return user.to_dict()

@app.post("/users")
def create_user(user: Users):
    user = User.User(conection)
    user.set_name(user.name)
    user.set_email(user.email)
    user.set_password(user.password)
    user.set_type(user.type)
    user.cadastrar()
    return user.to_dict()

@app.put("/users/{user_id}")
def update_user(user_id: int, user: Users):
    user = User.User(conection, user_id)
    user.buscar(user_id)
    user.set_name(user.name)
    user.set_email(user.email)
    user.set_password(user.password)
    user.set_type(user.type)
    user.atualizar()
    return user.to_dict()

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = User.User(conection, user_id)
    user.buscar(user_id)
    user.deletar()
    return user.to_dict()