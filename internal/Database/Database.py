from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    senha = Column(String(50), nullable=False)
    data_nascimento = Column(DateTime, nullable=False)
    cpf = Column(String(11), nullable=False)
    id_endereco = Column(Integer, ForeignKey('endereco.id'))
    endereco = relationship("Endereco")

class Cartao(Base):
    __tablename__ = 'cartao'
    id = Column(Integer, primary_key=True)
    numero_cartao = Column(String(266), nullable=False)
    codigo_cartao = Column(String(266), nullable=False)
    validade = Column(Date, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    limite_total = Column(Float, nullable=False)
    limite_disponivel = Column(Float, nullable=False)
    nome_cartao = Column(String(100), nullable=False)
    tipo_cartao = Column(String(50), nullable=False)
    usuario = relationship("User")

class Endereco(Base):
    __tablename__ = 'endereco'
    id = Column(Integer, primary_key=True)
    rua = Column(String(50), nullable=False)
    numero = Column(Integer, nullable=False)
    estado = Column(String(2), nullable=False)
    referencia = Column(String(50), nullable=False)
    usuario = relationship("User", back_populates="endereco")

class Entrada(Base):
    __tablename__ = 'entrada'
    id = Column(Integer, primary_key=True)
    descricao = Column(String(266), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    id_cartao = Column(Integer, ForeignKey('cartao.id'))
    usuario = relationship("User")
    valor = Column(DECIMAL(6,2), nullable=False)
    criado_em = Column(Date, nullable=False)
    atualizado_em = Column(Date, nullable=False)
    deletado_em = Column(Date, nullable=False)
    tag = Column(String(50), nullable=False)
    detalhes = Column(String(266), nullable=False)

class Saida(Base):
    __tablename__ = 'saida'
    id = Column(Integer, primary_key=True)
    descricao = Column(String(266), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    id_cartao = Column(Integer, ForeignKey('cartao.id'))
    usuario = relationship("User")
    valor = Column(DECIMAL(6,2), nullable=False)
    criado_em = Column(Date, nullable=False)
    atualizado_em = Column(Date, nullable=False)
    deletado_em = Column(Date, nullable=False)
    tag = Column(String(50), nullable=False)
    detalhes = Column(String(266), nullable=False)