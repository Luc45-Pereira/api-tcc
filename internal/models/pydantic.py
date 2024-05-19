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
    id_endereco: int

class endereco_model(BaseModel):
    rua: str
    numero: int
    estado: str
    referencia: str

class entrada_model(BaseModel):
    descricao: str
    id_usuario: int
    id_cartao: Optional[int]
    valor: float
    criado_em: str
    tag: str
    detalhes: str

class saida_model(BaseModel):
    descricao: str
    id_usuario: int
    id_cartao: Optional[int]
    valor: float
    criado_em: str
    tag: str
    detalhes: str

class cartao_model(BaseModel):
    numero_cartao: str
    codigo_cartao: str
    validade: str
    id_usuario: int
    limite_total: float
    limite_disponivel: float
    nome_cartao: str
    tipo_cartao: str