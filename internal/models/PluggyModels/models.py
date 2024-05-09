from pydantic import BaseModel
from typing import Optional


class token_model(BaseModel):
    access_token: str
    token: str


class accounts_model(BaseModel):
    """ Modelo para retorno das contas do pluggy """
    id: str
    type: str
    subtype: str
    name: str
    balance: float
    currencyCode: str
    itemId: str
    number: str
    createdAt: str
    updatedAt: str
    marketingName: str
    taxNumber: Optional[str]
    owner: Optional[str]
    bankData: Optional[dict]
    creditData: Optional[dict]

class transactions_model(BaseModel):
    """ Modelo para retorno das transacoes do pluggy """
    id: str
    description: str
    descriptionRaw: Optional[str]
    currencyCode: str
    amount: float
    amountInAccountCurrency: Optional[float]
    date: str
    category: str
    categoryId: str
    balance: Optional[float]
    accountId: str
    providerCode: Optional[str]
    status: str
    paymentData: Optional[dict]
    type: str
    creditCardMetadata: Optional[dict]
    acquirerData: Optional[dict]
    merchant: Optional[dict]
    createdAt: str
    updatedAt: str