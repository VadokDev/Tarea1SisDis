import socket

LOCALHOST = "0.0.0.0"
DATASERVER_PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((LOCALHOST, DATASERVER_PORT))

msg = ""
# envio mensajes hasta que ingreso "Terminar"
while msg != "Terminar":

    msg = input()
    cliente.send(bytes(msg, "utf-8"))

    data = cliente.recv(1024)
    print(data.decode("utf-8"))

print("Adios!")
cliente.close()