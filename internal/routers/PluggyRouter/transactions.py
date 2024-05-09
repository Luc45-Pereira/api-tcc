""" Rotas para lidar com as transações da conta bancaria """
from fastapi import APIRouter, Depends, HTTPException
import internal.Connection.conn as conn
import internal.Database.Database as Database
from internal.models.pydantic import token_model
from internal.models.PluggyModels.models import accounts_model, transactions_model
from internal.routers.PluggyRouter.access_pluggy import get_access_token
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

URL = os.getenv("PLUGGY_URL")

@router.get("/accounts")
async def get_accounts_of_transactions(payload: token_model = Depends()):
    """ Retorna todas as contas bancarias do usuário """
    try:
        # decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        url = f"{URL}/accounts?itemId={os.getenv('PLUGGY_APP_ID')}"

        headers = {
            "Content-Type": "application/json",
            "x-api-key": get_access_token()['apiKey'],
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        
        response_json = response.json()

        accounts_models = []

        for account in response_json['results']:
            account_model = accounts_model(**account)
            accounts_models.append(account_model)
        
        return accounts_models

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.post("/select_account")
async def select_account_of_transactions(account_id: str, payload: token_model = Depends()):
    """ Seleciona uma conta bancaria para ser a conta padrão """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session = Session.get_session()
        account_user = session.query(Database.Account).filter_by(id_usuario=decoded_token['user']).first()
        account_user.pluggy_account_id = account_id

        session.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")


@router.get("/")
async def get_transactions_of_account(payload: token_model = Depends()):
    """ Retorna todas as transações de uma conta bancaria """
    try:
        decoded_token = jwt.decode(payload.access_token, SECRET_KEY, algorithms=[ALGORITHM])

        session = Session.get_session()
        account_user = session.query(Database.Account).filter_by(id_usuario=decoded_token['user']).first()
        account_id = account_user.pluggy_account_id
        
        url = f"{URL}/transactions?accountId={account_id}"

        headers = {
            "Content-Type": "application/json",
            "x-api-key": get_access_token()['apiKey'],
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        
        response_json = response.json()

        transactions_models = []

        for transaction in response_json['results']:
            transaction_model = transactions_model(**transaction)
            transactions_models.append(transaction_model)
        
        return transactions_models

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Token inválido")