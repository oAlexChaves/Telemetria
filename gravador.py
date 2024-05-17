import customtkinter as ctk
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

# Configuração inicial do CTk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gravação de Corrida")
        self.geometry("400x600")

        self.label_p = ctk.CTkLabel(self, text="Valor de P:")
        self.label_p.pack(pady=10)
        self.entry_p = ctk.CTkEntry(self)
        self.entry_p.pack(pady=10)

        self.label_i = ctk.CTkLabel(self, text="Valor de I:")
        self.label_i.pack(pady=10)
        self.entry_i = ctk.CTkEntry(self)
        self.entry_i.pack(pady=10)

        self.label_d = ctk.CTkLabel(self, text="Valor de D:")
        self.label_d.pack(pady=10)
        self.entry_d = ctk.CTkEntry(self)
        self.entry_d.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="Iniciar Gravação", command=self.gravar_corrida)
        self.start_button.pack(pady=20)

        self.label_initial_speed = ctk.CTkLabel(self, text="")
        self.label_initial_speed.pack(pady=10)

        self.label_time_elapsed = ctk.CTkLabel(self, text="")
        self.label_time_elapsed.pack(pady=10)

    def gravar_corrida(self):
        try:
            ser = serial.Serial('COM3', 9600)  # Modifique para a porta e a taxa de baud do seu Arduino
            p = float(self.entry_p.get())
            i = float(self.entry_i.get())
            d = float(self.entry_d.get())

            # Envia os valores P, I, D ao Arduino
            ser.write(str(p).encode())
            ser.write(str(i).encode())
            ser.write(str(d).encode())

            initial_speed = float(ser.readline().decode().strip())
            self.label_initial_speed.configure(text=f"Velocidade Inicial: {initial_speed}")

            print("PID e velocidade inicial gravada!")

            erros = []

            # Aguarda mensagem de fim do Arduino
            print("Aguardando fim da corrida...")
            start_time = datetime.datetime.now()
            while True:
                line = ser.readline().decode().strip()
                if line == "END":
                    end_time = datetime.datetime.now()
                    print("Corrida finalizada!")
                    break

            tempo_decorrido = end_time - start_time
            tempo_decorrido_em_segundos = tempo_decorrido.total_seconds()
            self.label_time_elapsed.configure(text=f"Tempo Decorrido: {tempo_decorrido_em_segundos:.2f} segundos")

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
            corrida = Corrida(p=str(p), i=str(i), d=str(d), initial_speed=initial_speed, erros=erros_str,
                              conceito=int(conceito), tempo=tempo_decorrido_em_segundos,
                              seguiu_linha=seguiu_linha, oscilacao=oscilacao, observacao=observacao)

            session.add(corrida)
            session.commit()

            print("Dados gravados com sucesso.")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
