import socket, threading
import _thread
import time
import random
import logging

LOCALHOST = "0.0.0.0"
DATASERVER_PORT = 5000

# clase que interactua con los clientes
class ClientServerThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

        print(f"[Cliente] Conexión desde {self.clientAddress} establecida!")

    def run(self):
        msg = ""

        while(msg != "Terminar"):
            msg = self.clientSocket.recv(1024).decode("utf-8")
            #print(f"[Cliente {self.clientAddress}] {msg}")

            # guardo en archivo
            archivo = open("log.txt", "a")
            archivo.write(f"{self.clientAddress} - {msg}\n")
            archivo.close()
            # envio respuesta:
            try:
                self.clientSocket.send(bytes(f"Ok", "utf-8"))
            except BrokenPipeError as e:
                break # de no poder mandar mensajes, termino la conexión
        # termino la conexion
        print(f"[Cliente {self.clientAddress}] conexión terminada!")
        self.clientSocket.close()
                
# funcion main        
def Server():
    # inicializo el server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCALHOST, DATASERVER_PORT))
    server.listen(5)

    print("Server on")
    # escucha conexiones
    while True:
        clientSocket, clientAddress =  server.accept()
        
        # 3-step handshake
        msg = clientSocket.recv(1024).decode("utf-8") # recibo
        clientSocket.send(bytes("Hola", "utf-8")) # envio
        tipo = clientSocket.recv(1024).decode("utf-8") # recibo el tipo
        #print(f"Entro un {tipo}, de ip: {clientAddress}")

        # dependiendo del tipo interactua con un thread
        if tipo == "Cliente":
            newthread = ClientServerThread(clientAddress, clientSocket)
            newthread.start()
        else:
            print(f"Error al intentar el handshake con {clientAddress}")
            clientSocket.close()
        

Server()