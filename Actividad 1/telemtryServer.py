import socket, threading
import _thread
import time

LOCALHOST = "0.0.0.0"
DATASERVER_PORT = 5000

class DataServerThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
      threading.Thread.__init__(self)
      self.csocket = clientsocket
      self.clientAddress = clientAddress
      self.clientsocket = clientsocket      
      print("[DataServer] New connection added: ", self.clientAddress)

    def run(self):
        print("[DataServer] Connection from: ", self.clientAddress)

        msg = ''
        data = self.csocket.recv(1024)

        log = open("log.txt", "a")
        
        saludos = data.decode()
        print("[DataServer] Saludamiento: ", saludos)
        print("[DataServer] Monitoring initiated - Device")
        self.csocket.send("Ah! Soy saludado")
        
        log.write(saludos + '\n')
        log.close()

        while True:
            data = self.csocket.recv(1024)
            msg = data.decode()
            print("[DataServer]", msg) 
            self.csocket.send("OK")

        print("[DataServer]", self.clientAddress , " disconnected...")
        
def dataServer(threadName, delay):
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   server.bind((LOCALHOST, DATASERVER_PORT))
   print("DataServer started")
   while True:
       server.listen(1)
       clientsock, clientAddress = server.accept()
       newthread = DataServerThread(clientAddress, clientsock)
       newthread.start()

# Create two threads as follows
try:
   _thread.start_new_thread( dataServer, ("Thread-1", 2, ) )
except:
   print("Error: unable to start thread")

while 1:
   pass
