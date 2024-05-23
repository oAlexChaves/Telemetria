import random
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Corrida

# Criando a engine e conectando ao banco de dados SQLite
engine = create_engine('sqlite:///dados_corrida.db', echo=True)

Base = sqlalchemy.orm.declarative_base()

# Criando as tabelas no banco de dados, se não existirem
Base.metadata.create_all(engine)

# Criando uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()
def obter_dois_menores_tempos():
    resultados = session.query(Corrida).order_by(Corrida.tempo).limit(2).all()
    melhores_individuos = [(resultado.p, resultado.i, resultado.d) for resultado in resultados]
    return melhores_individuos

# Função para misturar aleatoriamente os valores de P, I e D
def misturar_valores(pai1, pai2):
    p1, i1, d1 = pai1
    p2, i2, d2 = pai2

    while True:
        novo_p1 = random.choice([p1, p2])
        novo_i1 = random.choice([i1, i2])
        novo_d1 = random.choice([d1, d2])

        novo_p2 = random.choice([p1, p2])
        novo_i2 = random.choice([i1, i2])
        novo_d2 = random.choice([d1, d2])

        # Verificar se os valores não são todos iguais
        if (novo_p1, novo_i1, novo_d1) != (novo_p2, novo_i2, novo_d2):
            # Aplica mutação nos valores de I e D para os dois novos indivíduos
            novo_i1 = mutacao(novo_i1)
            novo_d1 = mutacao(novo_d1)

            novo_i2 = mutacao(novo_i2)
            novo_d2 = mutacao(novo_d2)

            return (novo_p1, novo_i1, novo_d1), (novo_p2, novo_i2, novo_d2)

def mutacao(valor):
    # Aplica uma mutação de ±10% no valor fornecido
    mutacao_fator = random.uniform(-0.1, 0.1)
    valor_mutado = valor + valor * mutacao_fator
    return valor_mutado

# Algoritmo genético
def algoritmo_genetico():
    dois_menores_tempos = obter_dois_menores_tempos()
    populacao = list(set(dois_menores_tempos))  # Garantindo que não haja duplicatas

    print("População inicial:")
    for individuo in populacao:
        print(f"P: {individuo[0]}, I: {individuo[1]}, D: {individuo[2]}")

    if len(populacao) < 2:
        print("Não há pelo menos dois melhores indivíduos disponíveis para mistura.")
    else:
        novo_individuo1, novo_individuo2 = misturar_valores(populacao[0], populacao[1])
        print("\nDois novos conjuntos de valores de P, I e D após mistura:")
        print(f"Conjunto 1: P={novo_individuo1[0]}, I={novo_individuo1[1]}, D={novo_individuo1[2]}")
        print(f"Conjunto 2: P={novo_individuo2[0]}, I={novo_individuo2[1]}, D={novo_individuo2[2]}")

# Executar o AG
algoritmo_genetico()