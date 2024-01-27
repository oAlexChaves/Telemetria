from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Robo(Base):
    __tablename__ = 'corridas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    P = Column(Float)
    I = Column(Float)
    D = Column(Float)
    initial_speed = Column(Float)
    conceito = Column(Integer)
    sensores = Column(String)
    sensores_erro = Column(String)
    dataHora = Column(DateTime)
    tempo = Column(String)
    numeroTeste = Column(String)
