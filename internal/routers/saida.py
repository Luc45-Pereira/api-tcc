""" Rotas para lidar com as requisições HTTP relacionadas ao saida """
from fastapi import APIRouter, Depends, HTTPException
import internal.Connection.conn as conn
import internal.Database.Database as Database
from internal.models.pydantic import saida_model, token_model
import jwt
import os
import dotenv
import datetime

dotenv.load_dotenv()

Session = conn.Session()
router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

@router.get("/saidas/{user_id}")
async def read_saidas(user_id:int, payload: token_model = Depends()):
    """ Retorna todos os saidas cadastrados no banco de dados """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        saidas = session.query(Database.Saida).filter(Database.Saida.id_usuario == user_id ).all()
        for saida in saidas:
            print(saida.__dict__)
        return saidas

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.get("/{saida_id}")
async def read_saida(saida_id: int, payload: token_model = Depends()):
    """ Retorna um saida específico """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        saida = session.query(Database.Saida).filter(Database.Saida.id == saida_id).first()
        print(saida.__dict__)
        return saida

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.post("/")
async def create_saida(new_saida: saida_model, payload: token_model = Depends()):
    """ Cria um nova saida """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(new_saida)
        session = Session.get_session()
        saida = Database.Saida(descricao=new_saida.descricao, id_usuario=new_saida.id_usuario, valor=new_saida.valor, criado_em=datetime.datetime.now().date(), tag=new_saida.tag, detalhes=new_saida.detalhes)
        session.add(saida)
        session.commit()
        saida = session.query(Database.Saida).filter(Database.Saida.descricao == new_saida.descricao and Database.Saida.valor == new_saida.valor).first()

        return saida
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.put("/update/{saida_id}")
async def update_saida(saida_id: int, new_saida: saida_model,  payload: token_model = Depends()):
    """ Atualiza os dados de um saida """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        saida = session.query(Database.Saida).filter(Database.Saida.id == saida_id).first()
        saida.descricao = new_saida.descricao
        saida.valor = new_saida.valor
        saida.tag = new_saida.tag
        saida.detalhes = new_saida.detalhes
        session.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.delete("/delete/{saida_id}")
async def delete_saida(saida_id: int, payload: token_model = Depends()):
    """ Deleta um saida """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(decoded_token)
        session = Session.get_session()
        saida = session.query(Database.Saida).filter(Database.Saida.id == saida_id).first()
        session.delete(saida)
        session.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")