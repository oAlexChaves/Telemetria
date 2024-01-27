from datetime import date
class Robo_corrida:
    def __init__(self):
        self.P = 0.0
        self.I = 0.0
        self.D = 0.0
        self.initial_speed = 0.0
        self.conceito = 0
        self.sensores = []
        self.sensores_erro = []
        self.dataHora = ""
        self.tempo = ""
        self.numeroTeste = ""

    # Função para alterar o valor de P
    def alterar_P(self, novo_valor_P):
        self.P = novo_valor_P

    # Função para alterar o valor de I
    def alterar_I(self, novo_valor_I):
        self.I = novo_valor_I

    # Função para alterar o valor de D
    def alterar_D(self, novo_valor_D):
        self.D = novo_valor_D

    # Função para alterar o valor de initial_speed
    def alterar_initial_speed(self, novo_valor_initial_speed):
        self.initial_speed = novo_valor_initial_speed
    # Função para alterar o conceito
    def alterar_conceito(self, novo_conceito):
        self.conceito = novo_conceito

    # Função para adicionar um novo sensor
    def adicionar_sensor(self, novo_sensor):
        self.sensores.append(novo_sensor)

    # Função para adicionar um novo sensor de erro
    def adicionar_sensor_erro(self, novo_sensor_erro):
        self.sensores_erro.append(novo_sensor_erro)

    # Função para alterar a data e hora
    def alterar_data_hora(self, nova_data_hora):
        self.dataHora = nova_data_hora

    # Função para alterar o tempo
    def alterar_tempo(self, novo_tempo):
        self.tempo = novo_tempo

    # Função para alterar o número do teste
    def alterar_numero_teste(self, novo_numero_teste):
        self.numeroTeste = novo_numero_teste