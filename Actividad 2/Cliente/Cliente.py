import socket
import random
import time

# guardo en una lista distintas frases que enviara el cliente
def procesamiento():
    lista = list()
    # archivo con las distintas frases a usar
    file = open("mensaje.txt", "r") 

    for i in file:
        lista.append(i.strip())
    file.close()

    return lista

# constantes
SERVERIP = "server"
DATASERVER_PORT = 5000
MENSAJE = procesamiento()

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((SERVERIP, DATASERVER_PORT))

# 3-step handshake
cliente.send(bytes("Hola", "utf-8")) # envio
msg = cliente.recv(1024).decode("utf-8") # rebibo
cliente.send(bytes("Cliente", "utf-8")) # envio mi tipo
print(msg)
# envio mensajes hasta que ingreso "Terminar"
while msg != "Terminar":
    # elegimos el mensaje de forma aleatoria
    i = random.randint(1,100)
    if i == 1:
        msg = "Terminar"
    else:
        msg = random.choice(MENSAJE)
    #print(msg)
    #envio al server
    cliente.send(bytes(msg, "utf-8"))

    data = cliente.recv(1024)
    print(data.decode("utf-8"))
    time.sleep(0.1)

print("Adios!")
cliente.close()