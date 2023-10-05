""" Rotas para lidar com as requisições HTTP relacionadas ao endereco """
from fastapi import APIRouter, Depends, HTTPException
import internal.Connection.conn as conn
import internal.Database.Database as Database
from app.models.pydantic import endereco_model, token_model
import jwt
import os
import dotenv

dotenv.load_dotenv()

Session = conn.Session()
router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

@router.get("/enderecos")
async def read_users( payload: token_model = Depends()):
    """ Retorna todos os enderecos cadastrados no banco de dados """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        enderecos = session.query(Database.Endereco).all()
        for endereco in enderecos:
            print(endereco.__dict__)
        return enderecos

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.get("/{endereco_id}")
async def read_user(endereco_id: int, payload: token_model = Depends()):
    """ Retorna um endereco específico """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        endereco = session.query(Database.Endereco).filter(Database.Endereco.id == endereco_id).first()
        print(endereco.__dict__)
        return endereco

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.post("/")
async def create_user(new_endereco: endereco_model):
    """ Cria um novo endereco """
    print(new_endereco)
    session = Session.get_session()
    endereco = Database.User(rua=new_endereco.rua, numero=new_endereco.numero, estado=new_endereco.estado, referencia=new_endereco.referencia)
    session.add(endereco)
    session.commit()


@router.put("/update/{endereco_id}")
async def update_user(endereco_id: int, new_endereco: endereco_model,  payload: token_model = Depends()):
    """ Atualiza os dados de um endereco """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        endereco = session.query(Database.Endereco).filter(Database.Endereco.id == endereco_id).first()
        endereco.rua = new_endereco.rua
        endereco.numero = new_endereco.numero
        endereco.estado = new_endereco.estado
        endereco.referencia = new_endereco.referencia
        session.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.delete("/delete/{endereco_id}")
async def delete_user(endereco_id: int, payload: token_model = Depends()):
    """ Deleta um endereco """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(decoded_token)
        session = Session.get_session()
        endereco = session.query(Database.Endereco).filter(Database.Endereco.id == endereco_id).first()
        session.delete(endereco)
        session.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")