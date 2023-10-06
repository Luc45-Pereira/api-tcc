""" Rotas para lidar com as requisições HTTP relacionadas ao entrada """
from fastapi import APIRouter, Depends, HTTPException
import internal.Connection.conn as conn
import internal.Database.Database as Database
from app.models.pydantic import entrada_model, token_model
import jwt
import os
import dotenv
import datetime

dotenv.load_dotenv()

Session = conn.Session()
router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

@router.get("/entradas/{user_id}")
async def read_entradas(user_id:int, payload: token_model = Depends()):
    """ Retorna todos os entradas cadastrados no banco de dados """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        entradas = session.query(Database.Entrada).filter(Database.Entrada.id_usuario == user_id ).all()
        for entrada in entradas:
            print(entrada.__dict__)
        return entradas

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.get("/{entrada_id}")
async def read_entrada(entrada_id: int, payload: token_model = Depends()):
    """ Retorna um entrada específico """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        entrada = session.query(Database.Entrada).filter(Database.Entrada.id == entrada_id).first()
        print(entrada.__dict__)
        return entrada

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.post("/")
async def create_entrada(new_entrada: entrada_model):
    """ Cria um nova entrada """
    print(new_entrada)
    session = Session.get_session()
    entrada = Database.Entrada(descricao=new_entrada.descricao, id_usuario=new_entrada.id_usuario, valor=new_entrada.valor, criado_em=datetime.datetime.now().date(), tag=new_entrada.tag, detalhes=new_entrada.detalhes)
    session.add(entrada)
    session.commit()
    entrada = session.query(Database.Entrada).filter(Database.Entrada.descricao == new_entrada.descricao and Database.Entrada.valor == new_entrada.valor).first()

    return entrada


@router.put("/update/{entrada_id}")
async def update_entrada(entrada_id: int, new_entrada: entrada_model,  payload: token_model = Depends()):
    """ Atualiza os dados de um entrada """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        entrada = session.query(Database.Entrada).filter(Database.Entrada.id == entrada_id).first()
        entrada.descricao = new_entrada.descricao
        entrada.valor = new_entrada.valor
        entrada.tag = new_entrada.tag
        entrada.detalhes = new_entrada.detalhes
        session.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.delete("/delete/{entrada_id}")
async def delete_entrada(entrada_id: int, payload: token_model = Depends()):
    """ Deleta um entrada """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(decoded_token)
        session = Session.get_session()
        entrada = session.query(Database.Entrada).filter(Database.Entrada.id == entrada_id).first()
        session.delete(entrada)
        session.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")