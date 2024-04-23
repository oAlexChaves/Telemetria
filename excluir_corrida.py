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
        print()

def apagar_corrida():
    id_corrida = int(input("Digite o ID da corrida que deseja apagar: "))

    # Consulta a corrida pelo ID fornecido
    corrida = session.query(Corrida).filter_by(id=id_corrida).first()

    if corrida:
        # Remove a corrida da sessão e do banco de dados
        session.delete(corrida)
        session.commit()
        print("Corrida apagada com sucesso.")

        # Renumerar IDs
        corridas_remanescentes = session.query(Corrida).filter(Corrida.id > id_corrida).all()
        for corrida in corridas_remanescentes:
            corrida.id -= 1
        session.commit()
        print("IDs renumerados com sucesso.")
    else:
        print("Corrida não encontrada.")

if __name__ == "__main__":
    visualizar_corridas()
    apagar_corrida()
