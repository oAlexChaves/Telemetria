import serial

porta = 'COM1'
velocidade = 9600
ser = serial.Serial(porta, velocidade, timeout=1)

