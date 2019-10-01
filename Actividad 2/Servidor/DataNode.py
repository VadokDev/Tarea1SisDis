import socket, threading
import _thread
import time
LOCALHOST = "0.0.0.0"
DATASERVER_PORT = 5000

datanode = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
datanode.connect((LOCALHOST, DATASERVER_PORT))

datanode.send(bytes("Datanode", "utf-8"))
msg = datanode.recv(1024).decode("utf-8")
print(msg)

while msg != "Terminar":

    data = datanode.recv(1024).decode("utf-8")

    if data == "hearbeat":
        datanode.send(bytes("I'm fine", "utf-8"))
    elif data[:7] == "mensaje":
        archivo = open("data.txt", "a")
        archivo.write(data[8:] + "\n")
        archivo.close()
        datanode.send(bytes("It's fine", "utf-8"))

print("Adios!")
datanode.close()