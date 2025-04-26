from scapy.all import *
import os

# Función para recibir los paquetes y guardar el contenido
def receiveAndSaveFile(interface):
    print("[+][RECEIVER] Esperando paquetes...")

    fileName = None  # Para almacenar el nombre del archivo recibido
    _file    = None

    # Función de callback para procesar los paquetes recibidos
    def processPacket(packet):
        nonlocal fileName
        nonlocal _file
        identifyFileName    = b"1a2b3c4d"
        identifyFileContent = b"5e6f7g8h"
        writringDirectory   = "./OUTPUT"

        if packet.haslayer(TCP) and packet.haslayer(Raw):
            packetData = packet[Raw].load

            # El paquete que contiene el valor de la variable "identifyFileName" contiene el nombre del archivo
            if identifyFileName in packetData:
                fileName    = packetData[8:].decode()  # Extraer el nombre del archivo
                print(f"\n[+] Recibiendo archivo: {fileName}")
                # Crear fichero
                filePath = os.path.join(writringDirectory, fileName)
                _file = open(filePath, "wb")
            # Guardar el contenido del archivo
            elif identifyFileContent in packetData:
                print(f"[+] Tamaño paquete recibido: {len(packetData)} bytes.")
                fileContent = packetData[8:] # Extraer el contenido del fichero enviado
                _file.write(fileContent)
            elif packetData == b"\0":
                print(f"[+] Fichero recibido.")
                _file.close()
            else:
                pass

    # Escuchar en la interfaz especificada y procesar los paquetes
    sniff(iface=interface, prn=processPacket, store=0)

def main():
    # Ruta del directorio de registro de ficheros
    directoryPath = "./OUTPUT"
    # Verificar si el directorio no existe y crear
    if not os.path.exists(directoryPath): os.makedirs(directoryPath)
    # Recibir y guardar el archivo
    receiveAndSaveFile("eth0")  # Asegúrate de usar tu interfaz de red correcta

main()