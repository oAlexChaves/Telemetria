import serial
import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Corrida

# Criação da engine e conexão ao banco de dados SQLite
engine = create_engine('sqlite:///dados_corrida.db', echo=False)

# Base para o ORM e criação das tabelas, se não existirem
Base = sqlalchemy.orm.declarative_base()
Base.metadata.create_all(engine)

# Criação de uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

def gravar_corrida_manual():
    try:

        # Escolha da porta do robô
        porta_robo = choose_port()
        if porta_robo is None:
            print("Nenhuma porta selecionada.")
            return

        # Escolha da porta do portal
        print("Selecione a porta do portal:")
        porta_portal = choose_port()
        if porta_portal is None:
            print("Nenhuma porta selecionada.")
            return
        
        try:
            ser_robo = serial.Serial(porta_robo, 9600)
            ser_portal = serial.Serial(porta_portal, 9600)
        except Exception as e:
            raise Exception(f"Erro ao conectar às portas seriais: {e}")

        # Captura dos valores PID e velocidade inicial
        try:
            p = float(input("Digite o valor de P: "))
            i = float(input("Digite o valor de I: "))
            d = float(input("Digite o valor de D: "))
            initial_speed = float(input("Digite o valor de da velocidade inicial: "))

        except ValueError:
            raise ValueError("Valores de P, I, D e velocidade inicial devem ser números")

        # Envia os valores P, I, D ao Arduino
        pid_values = f"pid {p} {i} {d} {initial_speed}\n"
        ser_robo.write(pid_values.encode())
        ser_robo.write("end".encode())  # Correção: adicionando parênteses ao `.encode()`
        ser_robo.flush()

        print(f"Velocidade Inicial: {initial_speed}")
        print("PID e velocidade inicial gravada!")

        erros = []

        # Aguarda mensagem de início do Arduino
        while True:
            line = ser_portal.readline().decode('utf-8', errors='ignore').strip()
            if line == "START":
                ser_portal.write('funcionando'.encode())
                start_time = datetime.datetime.now()
                print("Corrida Começou!")
                break
        print("Aguardando fim da corrida...")

        # Aguarda mensagem de fim do Arduino
        while True:
            line = ser_portal.readline().decode('utf-8', errors='ignore').strip()
            if line == "END":
                ser_portal.write('finalizado'.encode())
                end_time = datetime.datetime.now()
                print("Corrida finalizada!")
                break

        # Calcula o tempo decorrido e exibe
        tempo_decorrido = end_time - start_time
        tempo_decorrido_em_segundos = tempo_decorrido.total_seconds()
        print(f"Tempo Decorrido: {tempo_decorrido_em_segundos:.2f} segundos")

        ser.close()

        # Pergunta sobre o desempenho do robô
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
                else:
                    conceito = 1
                    oscilacao = None
                    break
            else:
                print("Resposta inválida. Por favor, responda 'sim' ou 'não'.")

        # Coleta uma observação e armazena no banco de dados
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


import serial.tools.list_ports

def choose_port():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("Nenhuma porta serial disponível.")
        return None

    print("Selecione a porta desejada:")
    for i, port in enumerate(ports, start=1):
        print(f"{i}. {port.device} - {port.description}")

    try:
        choice = int(input("Digite o número da porta que deseja utilizar: "))
        if 1 <= choice <= len(ports):
            selected_port = ports[choice - 1].device
            print(f"Você selecionou a porta: {selected_port}")
            return selected_port
        else:
            print("Escolha inválida. Número fora do intervalo.")
            return None
    except ValueError:
        print("Entrada inválida. Digite um número.")
        return None


if __name__ == "__main__":
    gravar_corrida_manual()
