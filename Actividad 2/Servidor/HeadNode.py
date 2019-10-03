import socket, threading
import _thread
import time
import random
import logging

LOCALHOST = "0.0.0.0"
DATASERVER_PORT = 5000

# clase que se usa para hacer hearbeat
class HearBeat(threading.Thread):
    def __init__(self, lista):
        threading.Thread.__init__(self)
        self.lista = lista # lista con los DataNode disponibles

    def run(self):
        while True:
            time.sleep(5) # heart de 5 segundos
            # aqui me comunico con los DataNode
            for dataSocket, dataAddress in self.lista:
                try:
                    # envio el mensaje
                    dataSocket.send(bytes("hearbeat", "utf-8"))
                    msg = dataSocket.recv(1024).decode("utf-8") # recibo el mensaje
                    #print(f"Comunicacion de {dataAddress}: {msg}")
                    logging.info(f"{dataAddress[0]}:{dataAddress[1]}")
                except BrokenPipeError as e:
                    self.lista.remove((dataSocket, dataAddress))
                    logging.info(f"Termino conexion de {dataAddress[0]}:{dataAddress[1]}")
                    print(f"[Data {dataAddress[0]}:{dataAddress[1]}] conexión terminada!")

    def enviar(self, mensaje):
        dataSocket, dataAddress = random.choice(self.lista) # elijo uno de los 3
        msg = "mensaje " + mensaje
        try:
            # envio el mensaje
            dataSocket.send(bytes(msg, "utf-8"))
            respuesta = dataSocket.recv(1024).decode("utf-8") # recibo el mensaje
            #print(f"Comunicacion de {dataAddress}: {respuesta}")
            return dataAddress
        except BrokenPipeError as e:
            self.lista.remove((dataSocket, dataAddress))
            print(f"[Cliente {dataAddress[0]}:{dataAddress[1]}] conexión terminada!")
            return self.enviar(mensaje) # de fallar intento con otro

# clase que interactua con los clientes
class ClientServerThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket, hearBeat):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.hearBeat = hearBeat

        #print(f"[Cliente] Conexión desde {self.clientAddress} establecida!")

    def run(self):
        msg = ""

        while(msg != "Terminar"):
            msg = self.clientSocket.recv(1024).decode("utf-8")
            #print(f"[Cliente {self.clientAddress}] {msg}")

            # almaceno el mensaje
            address = self.hearBeat.enviar(msg)

            # guardo en archivo
            arch = open("registro_server.txt", "a")
            arch.write(f"{time.ctime()} - {address[0]}:{address[1]} guardo mensaje de {self.clientAddress[0]}:{self.clientAddress[1]}\n")
            arch.close()
            # envio respuesta:
            try:
                self.clientSocket.send(bytes(f"Ok {address}", "utf-8"))
            except BrokenPipeError as e:
                break # de no poder mandar mensajes, termino la conexión
        # termino la conexion
        print(f"[Cliente {self.clientAddress}] conexión terminada!")
        self.clientSocket.close()
                
# funcion main        
def Server():
    # creo los logs
    logging.basicConfig(filename='hearbeat_server.txt'
    , format='[%(asctime)s] - %(message)s'
    , datefmt='%H:%M:%S'
    , level=logging.INFO
    , filemode='a')

    # inicializo el server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCALHOST, DATASERVER_PORT))
    server.listen(15)

    # creo el HearBeat de DataNodes
    list_data = list() # guardo los DataNode que tenga
    hear = HearBeat(list_data)
    hear.start()
    print("Server on")
    # escucha conexiones
    while True:
        clientSocket, clientAddress =  server.accept()
        
        # 3-step handshake
        msg = clientSocket.recv(1024).decode("utf-8") # recibo
        clientSocket.send(bytes("Hola", "utf-8")) # envio
        tipo = clientSocket.recv(1024).decode("utf-8") # recibo el tipo
        print(f"Entro un {tipo}, de ip: {clientAddress}")

        # dependiendo del tipo interactua con un thread
        if tipo == "Cliente":
            newthread = ClientServerThread(clientAddress, clientSocket, hear)
            newthread.start()
        elif tipo == "Data":
            list_data.append((clientSocket, clientAddress))
        else:
            print(f"Error al intentar el handshake con {clientAddress}")
            clientSocket.close()
        

Server()