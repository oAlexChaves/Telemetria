import serial
import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from algoritmo_genetico import algoritmo_genetico
from gravadormanual import choose_port
from models import Corrida

# Criação da engine e conexão ao banco de dados SQLite
engine = create_engine('sqlite:///dados_corrida.db', echo=False)

# Base para o ORM e criação das tabelas, se não existirem
Base = sqlalchemy.orm.declarative_base()
Base.metadata.create_all(engine)

# Criação de uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

def gravar_corrida_com_genetico():
    try:
        # Obtenção dos valores PID pelo algoritmo genético
        novos_individuos = algoritmo_genetico()
        print("\nValores de PID gerados pelo algoritmo genético:")
        for idx, (p, i, d) in enumerate(novos_individuos, start=1):
            print(f"{idx}. P={p:.2f}, I={i:.2f}, D={d:.2f}")

        # Seleção do conjunto de valores de PID
        while True:
            escolha = input("Selecione o conjunto de PID (1 ou 2): ")
            if escolha in ["1", "2"]:
                escolhido = novos_individuos[int(escolha) - 1]
                p, i, d = escolhido
                break
            else:
                print("Escolha inválida. Digite 1 ou 2.")

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

        # Captura da velocidade inicial
        try:
            initial_speed = float(input("Digite o valor da velocidade inicial: "))
        except ValueError:
            raise ValueError("Velocidade inicial deve ser um número")

        # Envio dos valores PID e velocidade inicial ao Arduino do robô
        pid_values = f"pid {p} {i} {d} {initial_speed}\n"
        ser_robo.write(pid_values.encode())
        ser_robo.write("end".encode())
        ser_robo.flush()

        print(f"Velocidade Inicial: {initial_speed}")
        print(f"PID enviado: P={p:.2f}, I={i:.2f}, D={d:.2f}")

        print("Aguardando corrida e coletando resultados...")

        # Aguarda mensagem de início do portal
        while True:
            line = ser_portal.readline().decode('utf-8', errors='ignore').strip()
            if line == "START":
                start_time = datetime.datetime.now()
                print("Corrida Começou!")
                break

        print("Aguardando fim da corrida...")

        # Aguarda mensagem de fim do portal
        while True:
            line = ser_portal.readline().decode('utf-8', errors='ignore').strip()
            if line == "END":
                end_time = datetime.datetime.now()
                print("Corrida finalizada!")
                break

        # Calcula o tempo decorrido e exibe
        tempo_decorrido = end_time - start_time
        tempo_decorrido_em_segundos = tempo_decorrido.total_seconds()
        print(f"Tempo Decorrido: {tempo_decorrido_em_segundos:.2f} segundos")

        # Fecha conexões
        ser_robo.close()
        ser_portal.close()

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

        corrida = Corrida(p=p, i=i, d=d, initial_speed=initial_speed,
                          conceito=int(conceito), tempo=tempo_decorrido_em_segundos,
                          seguiu_linha=seguiu_linha, oscilacao=oscilacao, observacao=observacao)

        session.add(corrida)
        session.commit()

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    gravar_corrida_com_genetico()
