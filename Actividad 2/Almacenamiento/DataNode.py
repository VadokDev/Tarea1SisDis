import socket
import logging

SERVERIP = "server" # definido en docker-compose
DATASERVER_PORT = 5000

datanode = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
datanode.connect((SERVERIP, DATASERVER_PORT))

# logs
logging.basicConfig(filename='data.txt'
, format='[%(asctime)s] - %(message)s'
, datefmt='%H:%M:%S'
, level=logging.INFO
, filemode='a')

# 3-step handshake
datanode.send(bytes("Hola", "utf-8")) # envio
msg = datanode.recv(1024).decode("utf-8") # rebibo
datanode.send(bytes("Data", "utf-8")) # envio mi tipo
print(msg)

while msg != "Terminar":

    msg = datanode.recv(1024).decode("utf-8") # recibo un mensaje del server

    #print(f"Mensaje recibido: {msg}")
    # recibo heartbeat
    if msg == "hearbeat":
        datanode.send(bytes("I'm fine", "utf-8"))
    # en cambio, si es un mensaje:
    elif msg[:7] == "mensaje":
        logging.info(f"{socket.gethostbyname(socket.gethostname())} - {msg[8:]}")
        datanode.send(bytes("It's fine", "utf-8"))

print("Adios!")
datanode.close()