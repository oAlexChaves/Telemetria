import serial
import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Corrida
from teste_porta import find_port

# Criando a engine e conectando ao banco de dados SQLite
engine = create_engine('sqlite:///dados_corrida.db', echo=False)

Base = sqlalchemy.orm.declarative_base()

# Criando as tabelas no banco de dados, se não existirem
Base.metadata.create_all(engine)

# Criando uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

def gravar_corrida():
    try:
        ser = None
        keyword = "porta de saída"
        porta_robo = find_port(keyword)

        try:
            ser = serial.Serial(porta_robo, 9600)  # Modifique para a porta e a taxa de baud do seu Arduino
        except Exception as e:
            raise Exception(f"Erro ao conectar à porta serial: {e}")

        try:
            p = float(input("Digite o valor de P: "))
            i = float(input("Digite o valor de I: "))
            d = float(input("Digite o valor de D: "))
            initial_speed = float(input("Digite o valor de da velocidade inicial: "))
        except ValueError:
            raise ValueError("Valores de P, I, D e velocidade inicial devem ser números")

        # Envia os valores P, I, D ao Arduino
        pid_values = f"{p} {i} {d} {initial_speed}\n"
        ser.write(pid_values.encode())
        ser.flush()  # Assegura que todos os dados sejam enviados

        print(f"Velocidade Inicial: {initial_speed}")
        print("PID e velocidade inicial gravada!")

        erros = []

        # Aguarda mensagem de fim do Arduino
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line == "START":
                ser.write('funcionando'.encode())
                start_time = datetime.datetime.now()
                print("Corrida Começou!")
                break
        print("Aguardando fim da corrida...")

        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line == "END":
                ser.write('finalizado'.encode())
                end_time = datetime.datetime.now()
                print("Corrida finalizada!")
                break

        tempo_decorrido = end_time - start_time
        tempo_decorrido_em_segundos = tempo_decorrido.total_seconds()
        print(f"Tempo Decorrido: {tempo_decorrido_em_segundos:.2f} segundos")

        ser.close()

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
                            print("Oscilação inválida. Por favor, digite um valor entre 1 e 5.")
                    break
                else:  # Se a resposta for "não"
                    conceito = 1
                    oscilacao = None
                    break
            else:
                print("Resposta inválida. Por favor, responda 'sim' ou 'não'.")

        observacao = input("Observação: ")

        erros_str = str(erros)
        corrida = Corrida(p=p, i=i, d=d, initial_speed=initial_speed, erros=erros_str,
                          conceito=int(conceito), tempo=tempo_decorrido_em_segundos,
                          seguiu_linha=seguiu_linha, oscilacao=oscilacao, observacao=observacao)

        session.add(corrida)
        session.commit()

        print("Dados gravados com sucesso.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()
 
if __name__ == "__main__":
    gravar_corrida()
