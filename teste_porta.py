import serial
import serial.tools.list_ports

def list_ports():
    ports = serial.tools.list_ports.comports()
    for i, port in enumerate(ports, start=1):
        print(f"{i}. Porta encontrada: {port.device} - {port.description}")

def find_port(keyword):
    print("Começando a busca...")
    ports = serial.tools.list_ports.comports()

    if not ports:
        print("Nenhuma porta disponível.")
        return None

    for port in ports:
        try:
            print(f"Testando porta {port.device}")
            ser = serial.Serial(port.device, 9600, timeout=1)
            ser.write("Porta achada".encode())
            response = ser.readline().decode().strip()
            if response == keyword:
                ser.write("Porta achada".encode())  # Escrevendo a mensagem na porta
                ser.close()
                return port.device
            ser.close()
        except serial.SerialException as e:
            print(f"Erro ao acessar {port.device}: {e}")
            break  # Se der erro, pula para a próxima porta
        except serial.SerialTimeoutException as e:
            print(f"Timeout na porta {port.device}: {e}")
            ser.close()
    return None


# Listar todas as portas disponíveis
list_ports()
find_port()