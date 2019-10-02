import socket, threading
import _thread
import time

LOCALHOST = "0.0.0.0"
DATASERVER_PORT = 5000

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
            print(f"[Cliente {self.clientAddress}] {msg}")

            # envio respuesta:
            try:
                self.clientSocket.send(bytes("Mensaje recibido", "utf-8"))
            except BrokenPipeError as e:
                break # de no poder mandar mensajes, termino la conexión
        # termino la conexion
        print(f"[Cliente {self.clientAddress}] conexión terminada!")
        self.clientSocket.close()

def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCALHOST, DATASERVER_PORT))
    server.listen(3)
    print("[Server] on")
    while True:
        clientSocket, clientAddress =  server.accept()
        
        # 3-step handshake
        
        msg = clientSocket.recv(1024).decode("utf-8") # recibo
        clientSocket.send(bytes("Hola", "utf-8")) # envio
        tipo = clientSocket.recv(1024).decode("utf-8") # recibo el tipo

        # dependiendo del tipo interactua con un thread
        if tipo == "Cliente":
            newthread = ClientServerThread(clientAddress, clientSocket)
            newthread.start()
        elif tipo == "Data":
            arch = open("test.txt", "a")
            arch.write(f"Entro el Data {clientAddress}\n")
            arch.close()
            clientSocket.close()
        else:
            print(f"Error al intentar el handshake con {clientAddress}")
        

Server()