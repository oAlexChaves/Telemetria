import serial
import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Corrida

# Criando a engine e conectando ao banco de dados SQLite
engine = create_engine('sqlite:///dados_corrida.db', echo=True)

Base = sqlalchemy.orm.declarative_base()

# Criando as tabelas no banco de dados, se não existirem
Base.metadata.create_all(engine)

# Criando uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()


def gravar_corrida():
    # Inicializa a comunicação serial com o Arduino
    ser = serial.Serial('COM3', 9600)  # Modifique para a porta e a taxa de baud do seu Arduino

    # Lê os valores da porta serial
    p = float(ser.readline().decode().strip())
    i = float(ser.readline().decode().strip())
    d = float(ser.readline().decode().strip())
    initial_speed = float(ser.readline().decode().strip())
    print("PID e velocidade incial gravada!!")
    # Lê os valores dos erros da porta serial
    erros = []
    for _ in range(10):
        erro = float(ser.readline().decode().strip())
        erros.append(erro)
        print(erro)

    # Fecha a comunicação serial
    ser.close()

    # Solicita o conceito da corrida
    while True:
        conceito = input("Digite o conceito da corrida (de 1 a 5): ")
        if conceito.isdigit() and 1 <= int(conceito) <= 5:
            break
        else:
            print("Conceito inválido. Por favor, digite um valor entre 1 e 5.")

    # Cria um novo objeto Corrida com os valores lidos
    erros_str = str(erros)  # Converte a lista de erros em uma string
    corrida = Corrida(p=p, i=i, d=d, initial_speed=initial_speed, erros=erros_str, conceito=int(conceito))

    # Adiciona a corrida à sessão
    session.add(corrida)
    # Commita as alterações (grava os dados no banco de dados)
    session.commit()

    print("Dados gravados com sucesso.")

gravar_corrida()
