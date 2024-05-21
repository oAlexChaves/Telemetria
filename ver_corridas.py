from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Corrida
# Criando a engine e conectando ao banco de dados SQLite
engine = create_engine('sqlite:///dados_corrida.db', echo=False)
# Criando uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()
def visualizar_corridas():
    # Consulta todas as corridas no banco de dados
    corridas = session.query(Corrida).all()
    # Exibe as informações de cada corrida
    # Lista para armazenar os dados formatados
    corridas_formatadas = []
    # Iterar sobre os registros e formatar os dados
    for corrida in corridas:
        corrida_formatada = {
            'ID': corrida.id,
            'P': round(corrida.p, 2),
            'I': round(corrida.i, 2),
            'D': round(corrida.d, 2),
            'Initial Speed': round(corrida.initial_speed, 2),
            'Erros': corrida.erros,
            'Conceito': corrida.conceito,
            'Seguiu Linha': corrida.seguiu_linha,
            'Tempo': corrida.tempo,
            'Oscilacao': corrida.oscilacao,
            'Observacao': corrida.observacao
        }
        corridas_formatadas.append(corrida_formatada)
    # Exibir os dados formatados como uma lista
    for corrida_formatada in corridas_formatadas:
        print(corrida_formatada)
if __name__ == "__main__":
    visualizar_corridas()