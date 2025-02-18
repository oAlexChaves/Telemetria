from sqlalchemy import Column, Float, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Corrida(Base):
    __tablename__ = 'corridas'

    id = Column(Integer, primary_key=True)
    p = Column(Float)
    i = Column(Float)
    d = Column(Float)
    initial_speed = Column(Float)
    erros = Column(Text)
    conceito = Column(Integer)  # Adicionando o campo 'conceito'
    seguiu_linha = Column(Text)
    tempo = Column(Integer)
    oscilacao = Column(Text)
    observacao = Column(Text)