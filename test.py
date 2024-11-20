import serial.tools.list_ports

def listar_portas_seriais():
    portas = serial.tools.list_ports.comports()
    lista_portas = [port.device for port in portas]
    if not lista_portas:
        print("Nenhuma porta serial encontrada")
    return lista_portas

portas_disponiveis = listar_portas_seriais()
print(portas_disponiveis)