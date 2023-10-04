from fastapi import APIRouter
import internal.Connection.conn as conn
import internal.Database.Database as Database
from app.models.pydantic import user_model


Session = conn.Session()
router = APIRouter()

@router.get("/users")
def read_users():
    session = Session.get_session()
    usuarios = session.query(Database.User).all()
    for usuario in usuarios:
        print(usuario.__dict__)
        print(usuario.endereco.__dict__)
    return usuarios


@router.get("/{user_id}")
def read_user(user_id: int):
    session = Session.get_session()
    usuario = session.query(Database.User).filter(Database.User.id == user_id).first()
    print(usuario.__dict__)
    print(usuario.endereco.__dict__)    
    return usuario


@router.post("/")
def create_user(new_user: user_model):
    print(new_user)
    session = Session.get_session()
    usuario = Database.User(nome=new_user.nome, email=new_user.email, senha=new_user.senha, data_nascimento=new_user.data_nascimento, cpf=new_user.cpf, id_endereco=new_user.id_endereco)
    session.add(usuario)
    session.commit()


@router.put("/update/{user_id}")
def update_user(user_id: int, new_user: user_model):
    session = Session.get_session()
    usuario = session.query(Database.User).filter(Database.User.id == user_id).first()
    usuario.nome = new_user.nome
    usuario.email = new_user.email
    usuario.senha = new_user.senha
    usuario.data_nascimento = new_user.data_nascimento
    usuario.cpf = new_user.cpf
    session.commit()


@router.delete("/delete/{user_id}")
def delete_user(user_id: int):
    session = Session.get_session()
    usuario = session.query(Database.User).filter(Database.User.id == user_id).first()
    session.delete(usuario)
    session.commit()
