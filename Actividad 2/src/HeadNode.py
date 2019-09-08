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
            data = self.clientSocket.recv(1024)
            msg = data.decode("utf-8")

            print(f"[Cliente {self.clientAddress}] {msg}")

            self.clientSocket.send(bytes("Mensaje recibido", "utf-8"))
        print(f"[Cliente {self.clientAddress}] conexión terminada!")
        self.clientSocket.close()

def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCALHOST, DATASERVER_PORT))
    server.listen(3)
    print("[Server] on")
    while True:
        clientSocket, clientAddress =  server.accept()
        newthread = ClientServerThread(clientAddress, clientSocket)
        newthread.start()

Server()