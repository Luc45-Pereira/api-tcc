from pydantic import BaseModel
from typing import Optional


class token_model(BaseModel):
    access_token: str


class user_model(BaseModel):
    nome: str
    email: str
    senha: str
    cpf: str
    data_nascimento: str
    id_endereco: Optional[int] = None

class endereco_model(BaseModel):
    rua: str
    numero: int
    estado: str
    referencia: str

class entrada_model(BaseModel):
    descricao: str
    id_usuario: int
    valor: float
    criado_em: str
    tag: str
    detalhes: str

class saida_model(BaseModel):
    descricao: str
    id_usuario: int
    valor: float
    criado_em: str
    tag: str
    detalhes: str