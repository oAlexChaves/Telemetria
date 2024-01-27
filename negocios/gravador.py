from conexoes.conexaoDB.conexaoDB import engine
from conexoes.conectarBT.conexaoBT import ser
from entities.corrida import Robo_corrida

engine.connect()
if ser.is_open:
    print(f"Conectado à porta {ser.porta} com sucesso!")
else:
    print(f"Falha ao conectar à porta {ser.porta}.")

corrida_atual = Robo_corrida

corrida_atual.alterar_P(ser.readline())
corrida_atual.alterar_I(ser.readline())
corrida_atual.alterar_D(ser.readline())
corrida_atual.alterar_initial_speed(ser.readline())
corrida_atual.alterar_data_hora(())
