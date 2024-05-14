import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import customtkinter as ctk
from models import Corrida


# Criando a engine e conectando ao banco de dados SQLite
engine = create_engine('sqlite:///dados_corrida.db', echo=True)

# Criando uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

def visualizar_corridas():
    # Consulta todas as corridas no banco de dados
    corridas = session.query(Corrida).all()

    # Criando uma nova janel
    app = ctk.CTk()
    app.geometry("600x500")
    app.title("LinePID Monitor")

    # Criando o Treeview para exibir as informações das corridas
    tree = ttk.Treeview(app)

    # Definindo as colunas da tabela
    tree["columns"] = ("ID", "P", "I", "D", "Velocidade Inicial", "Erros", "Conceito", "Seguiu a Linha", "Tempo", "Oscilação", "Observação")

    # Configurando as colunas
    tree.column("#0", width=0, stretch=tk.NO)  # Coluna oculta
    tree.column("ID", anchor=tk.CENTER, width=50)
    tree.column("P", anchor=tk.CENTER, width=50)
    tree.column("I", anchor=tk.CENTER, width=50)
    tree.column("D", anchor=tk.CENTER, width=50)
    tree.column("Velocidade Inicial", anchor=tk.CENTER, width=120)
    tree.column("Erros", anchor=tk.CENTER, width=50)
    tree.column("Conceito", anchor=tk.CENTER, width=80)
    tree.column("Seguiu a Linha", anchor=tk.CENTER, width=100)
    tree.column("Tempo", anchor=tk.CENTER, width=80)
    tree.column("Oscilação", anchor=tk.CENTER, width=80)
    tree.column("Observação", anchor=tk.CENTER, width=200)

    # Configurando os cabeçalhos das colunas
    tree.heading("#0", text="", anchor=tk.CENTER)
    tree.heading("ID", text="ID", anchor=tk.CENTER)
    tree.heading("P", text="P", anchor=tk.CENTER)
    tree.heading("I", text="I", anchor=tk.CENTER)
    tree.heading("D", text="D", anchor=tk.CENTER)
    tree.heading("Velocidade Inicial", text="Velocidade Inicial", anchor=tk.CENTER)
    tree.heading("Erros", text="Erros", anchor=tk.CENTER)
    tree.heading("Conceito", text="Conceito", anchor=tk.CENTER)
    tree.heading("Seguiu a Linha", text="Seguiu a Linha", anchor=tk.CENTER)
    tree.heading("Tempo", text="Tempo", anchor=tk.CENTER)
    tree.heading("Oscilação", text="Oscilação", anchor=tk.CENTER)
    tree.heading("Observação", text="Observação", anchor=tk.CENTER)

    # Adicionando as informações das corridas ao Treeview
    for corrida in corridas:
        tree.insert("", "end", text="",
                    values=(corrida.id, corrida.p, corrida.i, corrida.d, corrida.initial_speed,
                            corrida.erros, corrida.conceito, corrida.seguiu_linha, corrida.tempo,
                            corrida.oscilacao, corrida.observacao))

    # Exibindo o Treeview
    tree.pack(expand=True, fill=tk.BOTH)

    # Iniciando o loop principal da aplicação
    app.mainloop()

if __name__ == "__main__":
    visualizar_corridas()
