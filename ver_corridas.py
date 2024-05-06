from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Corrida

# Criando a engine e conectando ao banco de dados SQLite
engine = create_engine('sqlite:///dados_corrida.db', echo=True)

# Criando uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

def visualizar_corridas():
    # Consulta todas as corridas no banco de dados
    corridas = session.query(Corrida).all()

    # Exibe as informações de cada corrida
    for corrida in corridas:
        print(f"ID: {corrida.id}")
        print(f"P: {corrida.p}")
        print(f"I: {corrida.i}")
        print(f"D: {corrida.d}")
        print(f"Velocidade Inicial: {corrida.initial_speed}")
        print(f"Erros: {corrida.erros}")
        print(f"Conceito: {corrida.conceito}")
        print(f"Seguiu a Linha: {corrida.seguiu_linha}")  # Adiciona a exibição de 'seguir a linha'
        print(f"Tempo: {corrida.tempo}")  # Adiciona a exibição do tempo
        print(f"Oscilação: {corrida.oscilacao}")  # Adiciona a exibição da oscilação
        print(f"Observação: {corrida.observacao}")  # Adiciona a exibição da observação
        print()

if __name__ == "__main__":
    visualizar_corridas()
