import customtkinter
import serial
import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models import Corrida

# Criando a engine e conectando ao banco de dados SQLite
engine = create_engine('sqlite:///dados_corrida.db', echo=True)

Base = sqlalchemy.orm.declarative_base()

# Criando as tabelas no banco de dados, se não existirem
Base.metadata.create_all(engine)

# Criando uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

gravar_frame = customtkinter.CTk(app)


def gravar_corrida():

    ser = serial.Serial('COM3', 9600)  # Modifique para a porta e a taxa de baud do seu Arduino
    # Lê os valores da porta serial
    p = float(ser.readline().decode().strip())
    i = float(ser.readline().decode().strip())
    d = float(ser.readline().decode().strip())
    initial_speed = float(ser.readline().decode().strip())
    print("PID e velocidade incial gravada!!")
    # Lê os valores dos erros da porta serial
    erros = []
    start_time = datetime.datetime.now()  # Marca o tempo inicial
    for _ in range(10):
        erro = float(ser.readline().decode().strip())
        erros.append(erro)
        print(erro)
    end_time = datetime.datetime.now()  # Marca o tempo final

    # Calcula o tempo decorrido
    tempo_decorrido = end_time - start_time
    tempo_decorrido_em_segundos = tempo_decorrido.total_seconds()

    # Fecha a comunicação serial
    ser.close()

    # Pergunta se o robô seguiu a linha
    while True:
        seguiu_linha = input("O robô seguiu a linha? (sim/não): ").lower()
        if seguiu_linha in ["sim", "não", "nao"]:
            if seguiu_linha == "sim":
                while True:
                    conceito = input("Digite o conceito da corrida (de 1 a 5): ")
                    if conceito.isdigit() and 1 <= int(conceito) <= 5:
                        break
                    else:
                        print("Conceito inválido. Por favor, digite um valor entre 1 e 5.")
                while True:
                    oscilacao = input("Qual foi a oscilação do robô (de 1 a 5): ")
                    if oscilacao.isdigit() and 1 <= int(oscilacao) <= 5:
                        break
                    else:
                        print("Oscilacao inválida. Por favor, digite um valor entre 1 e 5.")
                break
            else:  # Se a resposta for "não"
                conceito = 1
                oscilacao = None
                break
        else:
            print("Resposta inválida. Por favor, responda 'sim' ou 'não'.")

    observacao = input("Observação: ")

    # Cria um novo objeto Corrida com os valores lidos
    erros_str = str(erros)  # Converte a lista de erros em uma string
    corrida = Corrida(p=p, i=i, d=d, initial_speed=initial_speed, erros=erros_str,
                      conceito=int(conceito), tempo=tempo_decorrido_em_segundos,
                      seguiu_linha=seguiu_linha, oscilacao=oscilacao, observacao=observacao)

    # Adiciona a corrida à sessão
    session.add(corrida)
    # Commita as alterações (grava os dados no banco de dados)
    session.commit()

    print("Dados gravados com sucesso.")


gravar_corrida()
