""" Rotas para lidar com as requisições HTTP relacionadas ao saida """
from fastapi import APIRouter, Depends, HTTPException
import internal.Connection.conn as conn
import internal.Database.Database as Database
from internal.models.pydantic import cartao_model, token_model
import jwt
import os
import dotenv
import datetime

dotenv.load_dotenv()

Session = conn.Session()
router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

@router.get("/")
async def read_cartoes(payload: token_model = Depends()):
    """ Retorna todos os cartoes do usuário """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_token["user"]
        session = Session.get_session()
        cartoes = session.query(Database.Cartao).filter(Database.Cartao.id_usuario == user_id ).all()
        for cartao in cartoes:
            print(cartao.__dict__)
        return cartoes

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.get("/{cartao_id}")
async def read_cartao(cartao_id: int, payload: token_model = Depends()):
    """ Retorna um cartao específico """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        cartao = session.query(Database.Cartao).filter(Database.Cartao.id == cartao_id).first()
        print(cartao.__dict__)
        return cartao

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.post("/")
async def create_cartao(new_cartao: cartao_model, payload: token_model = Depends()):
    """ Cria um nova cartao """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(new_cartao)
        session = Session.get_session()
        cartao = Database.Cartao(numero_cartao=new_cartao.numero_cartao, codigo_cartao=new_cartao.codigo_cartao, validade=new_cartao.validade, id_usuario=new_cartao.id_usuario, limite_total=new_cartao.limite_total, limite_disponivel=new_cartao.limite_disponivel, nome_cartao=new_cartao.nome_cartao, tipo_cartao=new_cartao.tipo_cartao)
        session.add(cartao)
        session.commit()
        cartao = session.query(Database.Cartao).filter(Database.Cartao.codigo_cartao == new_cartao.codigo_cartao).first()

        return cartao
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.put("/update/{cartao_id}")
async def update_cartao(cartao_id: int, new_cartao: cartao_model,  payload: token_model = Depends()):
    """ Atualiza os dados de um cartao """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        cartao = session.query(Database.Cartao).filter(Database.Cartao.id == cartao_id).first()
        cartao.numero_cartao = new_cartao.numero_cartao
        cartao.codigo_cartao = new_cartao.codigo_cartao
        cartao.validade = new_cartao.validade
        cartao.limite_total = new_cartao.limite_total
        cartao.limite_disponivel = new_cartao.limite_disponivel
        cartao.nome_cartao = new_cartao.nome_cartao
        cartao.tipo_cartao = new_cartao.tipo_cartao

        session.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.delete("/delete/{cartao_id}")
async def delete_saida(cartao_id: int, payload: token_model = Depends()):
    """ Deleta um saida """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(decoded_token)
        session = Session.get_session()
        cartao = session.query(Database.Cartao).filter(Database.Cartao.id == cartao_id).first()
        session.delete(cartao)
        session.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")