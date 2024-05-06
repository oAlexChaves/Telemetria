import serial.tools.list_ports

def find_port():
    for port in serial.tools.list_ports.comports():
        try:
            ser = serial.Serial(port.device)
            ser.write("porta de saída".encode())
            response = ser.readline().decode().strip()
            if response == "porta de saída":
                ser.write("Porta achada\n".encode())  # Escrevendo a mensagem na porta
                ser.close()
                return port.device
        except serial.SerialException:
            pass
    return None

keyword = "porta de saída"
port = find_port(keyword)
if port:
    print("Porta encontrada:", port)
else:
    print("Nenhuma porta encontrada com o texto:", keyword)
