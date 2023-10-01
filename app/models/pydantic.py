from pydantic import BaseModel

class user_model(BaseModel):
    nome: str
    email: str
    senha: str
    cpf: str
    data_nascimento: str
    id_endereco: int