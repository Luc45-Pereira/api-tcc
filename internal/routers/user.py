""" Rotas para lidar com as requisições HTTP relacionadas ao usuário """
from fastapi import APIRouter, Depends, HTTPException
import internal.Connection.conn as conn
import internal.Database.Database as Database
from internal.models.pydantic import user_model, token_model
from internal.Auth.token import Token
from sqlalchemy import and_
import jwt
import os
import dotenv
import hashlib

dotenv.load_dotenv()

Session = conn.Session()
router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

@router.get("/users")
async def read_users( payload: token_model = Depends()):
    """ Retorna todos os usuários cadastrados no banco de dados """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        usuarios = session.query(Database.User).all()
        for usuario in usuarios:
            print(usuario.__dict__)
            print(usuario.endereco.__dict__)
        return usuarios
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.get("/{user_id}")
async def read_user(user_id: int, payload: token_model = Depends()):
    """ Retorna um usuário específico """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        usuario = session.query(Database.User).filter(Database.User.id == user_id).first()
        print(usuario.__dict__)
        print(usuario.endereco.__dict__)    
        return usuario
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.post("/")
async def create_user(new_user: user_model):
    """ Cria um novo usuário """
    print(new_user)
    session = Session.get_session()
    usuario = Database.User(nome=new_user.nome, email=new_user.email, senha=hashlib.sha256(new_user.senha.encode()).hexdigest(), data_nascimento=new_user.data_nascimento, cpf=new_user.cpf, id_endereco=new_user.id_endereco)
    session.add(usuario)
    session.commit()


@router.put("/update/{user_id}")
async def update_user(user_id: int, new_user: user_model,  payload: token_model = Depends()):
    """ Atualiza os dados de um usuário """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        usuario = session.query(Database.User).filter(Database.User.id == user_id).first()
        usuario.nome = new_user.nome
        usuario.email = new_user.email
        usuario.senha = hashlib.sha256(new_user.senha.encode()).hexdigest()
        usuario.data_nascimento = new_user.data_nascimento
        usuario.cpf = new_user.cpf
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, payload: token_model = Depends()):
    """ Deleta um usuário """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(decoded_token)
        session = Session.get_session()
        usuario = session.query(Database.User).filter(Database.User.id == user_id).first()
        session.delete(usuario)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/login")
async def login(login, password: str):
    """ Realiza o login de um usuário """

    senha_hash = hashlib.sha256(password.encode()).hexdigest()

    session = Session.get_session()
    usuario = session.query(Database.User).filter(and_(Database.User.email == login, Database.User.senha == senha_hash)).first()
    if usuario is None:
        return {"status": "error", "message": "Usuário não encontrado"}
    
    token = Token(user_id=usuario.id, user_password=usuario.senha)
    token = token.generate_token()

    return {"status": "success", "message": "Usuário encontrado", "id": usuario.id, "token": token}