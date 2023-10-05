from pydantic import BaseModel


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