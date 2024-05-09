""" Rotas para lidar com conexao ao pluggy api """
from fastapi import APIRouter, Depends, HTTPException
import internal.Connection.conn as conn
import internal.Database.Database as Database
from internal.models.pydantic import cartao_model, token_model
import requests
import jwt
import os
import dotenv
import datetime

dotenv.load_dotenv()

Session = conn.Session()
router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

def get_access_token():
    """ Retorna o access token para a API do Pluggy """
    try:
        url = f"{os.getenv('PLUGGY_URL')}/auth"
        headers = {
            "Content-Type": "application/json",
        }
        body = {
            "clientId": os.getenv('PLUGGY_CLIENT_ID'),
            "clientSecret": os.getenv('PLUGGY_CLIENT_SECRET'),
        }

        response = requests.post(url, headers=headers, json=body)
        return response.json()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao buscar pluggy")


@router.get("/connectors")
async def get_connectors(payload: token_model = Depends()):
    """ Retorna todos os conectores disponíveis """
    try:
        url = f"{os.getenv('PLUGGY_URL')}/connectors"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": get_access_token()['apiKey'],
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        response_json = response.json()

        return response_json

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")
    

@router.get("/connectors/{connector_id}")
async def create_connectors(payload: dict, connector_id: str, token: token_model = Depends()):
    """ Cria um novo conector """
    try:
        decoded_token = jwt.decode(token.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token interno inválido")


    try:
        url = f"{os.getenv('PLUGGY_URL')}/items"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": get_access_token()['apiKey'],
        }
        body = {
            "parameters": payload,
            "connectorId": int(connector_id),
            "products": ["TRANSACTIONS"],
        }
        print(body)
        response = requests.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        response_json = response.json()
        try:
            account_user = Database.Account(id_usuario=decoded_token['user'], pluggy_connector_id=connector_id, pluggy_connection_id=response_json['id'])
            session = Session.get_session()
            session.add(account_user)
            session.commit()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Erro ao salvar conta")

        return response_json

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")