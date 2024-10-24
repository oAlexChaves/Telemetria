import serial.tools.list_ports

def find_port(keyword):
    # Lista todas as portas seriais disponíveis
    ports = list(serial.tools.list_ports.comports())
    
    if not ports:
        print("Nenhuma porta serial disponível.")
        return None
    
    print(f"Portas disponíveis: {[port.device for port in ports]}")

    # Verifica cada porta serial
    for port in ports:
        try:
            # Tenta abrir a porta serial com timeout aumentado para garantir que a leitura funcione
            ser = serial.Serial(port.device, 9600, timeout=5)
            
            print(f"Tentando comunicação com a porta {port.device}...")
            
            # Envia o comando com um newline para garantir que o ESP32 o processe corretamente
            ser.write("Porta achada\n".encode())
            
            # Aguarda uma resposta do ESP32
            response = ser.readline().decode().strip()  # Leitura da resposta
            print(f"Resposta recebida da porta {port.device}: {response}")
            
            # Se a resposta for a esperada, retorna a porta
            if response == keyword:
                ser.write("Porta achada\n".encode())  # Confirmação de que a porta foi encontrada
                ser.close()
                return port.device
            
            ser.close()  # Fecha a porta caso a resposta não seja a esperada
            
        except serial.SerialException as e:
            # Mostra o erro e continua para a próxima porta
            print(f"Erro de SerialException ao tentar se comunicar com {port.device}: {e}")
            continue  # Continua para a próxima porta

        except UnicodeDecodeError as e:
            # Mostra o erro de decodificação e continua para a próxima porta
            print(f"Erro de UnicodeDecodeError ao tentar se comunicar com {port.device}: {e}")
            continue  # Continua para a próxima porta

    return None  # Retorna None se nenhuma porta correta for encontrada

# Definindo o texto chave a ser encontrado
keyword = "porta de saída"
port = find_port(keyword)

# Verifica se a porta foi encontrada
if port:
    print("Porta encontrada:", port)
else:
    print("Nenhuma porta encontrada com o texto:", keyword)
