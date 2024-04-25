from sqlalchemy import create_engine, MetaData, Table, Column, Float, Integer, Text

# Criar uma instância de engine para o banco de dados SQLite
engine = create_engine('sqlite:///dados_corrida.db')

# Criar uma instância de MetaData
metadata = MetaData()

# Definir a estrutura da tabela 'corridas'
corridas = Table('corridas', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('p', Float),
                 Column('i', Float),
                 Column('d', Float),
                 Column('initial_speed', Float),
                 Column('erros', Text),
                 Column('conceito', Integer)  # Adicionando a coluna 'conceito'
                 )

# Criar o banco de dados e as tabelas, se ainda não existirem
metadata.create_all(engine)

print("Banco de dados e tabelas criados com sucesso.")
