import tkinter as tk
from tkinter import messagebox
import serial
import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session

from teste_porta import encontrar_porta_saida
from models import Corrida

# Função para gravar a corrida
def gravar_corrida():
    encontrar_porta_saida()
    porta_saida = encontrar_porta_saida()
    try:
        # Inicializa a comunicação serial com o Arduino
        ser = serial.Serial(porta_saida, 9600)  # Modifique para a porta e a taxa de baud do seu Arduino
    except serial.SerialException:
        messagebox.showerror("Erro", "Não foi possível conectar ao dispositivo serial.")
        return

    # Lê os valores da porta serial
    p = float(ser.readline().decode().strip())
    i = float(ser.readline().decode().strip())
    d = float(ser.readline().decode().strip())
    initial_speed = float(ser.readline().decode().strip())
    print("PID e velocidade inicial gravados!!")

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

    # Cria uma janela para interagir com o usuário
    window = tk.Tk()
    window.title("Informações da Corrida")
    tk.Label(window, text="O robô seguiu a linha? (sim/não):").pack()
    seguiu_linha_entry = tk.Entry(window)
    seguiu_linha_entry.pack()

    def submit():
        seguiu_linha = seguiu_linha_entry.get().lower()
        if seguiu_linha in ["sim", "não", "nao"]:
            if seguiu_linha == "sim":
                conceito = tk.simpledialog.askinteger("Conceito da Corrida", "Digite o conceito da corrida (de 1 a 5):")
                oscilacao = tk.simpledialog.askinteger("Oscilação do Robô", "Qual foi a oscilação do robô (de 1 a 5):")
            else:
                conceito = 1
                oscilacao = None

            observacao = tk.simpledialog.askstring("Observação", "Observação:")

            # Criar um novo objeto Corrida com os valores lidos
            erros_str = str(erros)  # Converte a lista de erros em uma string
            corrida = Corrida(p=p, i=i, d=d, initial_speed=initial_speed, erros=erros_str,
                              conceito=conceito, tempo=tempo_decorrido_em_segundos,
                              seguiu_linha=seguiu_linha, oscilacao=oscilacao, observacao=observacao)

            # Adiciona a corrida à sessão
            session.add(corrida)
            # Commita as alterações (grava os dados no banco de dados)
            session.commit()

            messagebox.showinfo("Sucesso", "Dados gravados com sucesso.")
            window.destroy()
        else:
            messagebox.showerror("Erro", "Resposta inválida. Por favor, responda 'sim' ou 'não'.")

    submit_button = tk.Button(window, text="Enviar", command=submit)
    submit_button.pack()

    window.mainloop()


# Chamada da função para gravar a corrida
gravar_corrida()
