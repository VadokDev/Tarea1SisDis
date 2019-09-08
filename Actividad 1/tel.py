import sys
import socket
import traceback
import time

def do_work( forever = True):
    while True:
        print "[Client] Starting connection"
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(None)

        x = sock.getsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE)
        if x == 0:
            print 'Socket Keepalive off, turning on'
            x = sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            print 'setsockopt=', x
        else:
            print 'Socket Keepalive already on'
        try:
            sock.connect(('localhost', 5000))

        except socket.error:
            print 'Socket connect failed! Loop up and try socket again'
            traceback.print_exc()
            time.sleep(5.0)
            continue

        print 'Socket connect worked!'
        saludo = False

        while 1:
            try:
                if not saludo:
                    sock.send("Saludamentacion")
                    req = sock.recv(1024)
                    saludo = True
                print req
                sock.send(input("Manda una wea: "))
                req = sock.recv(1024)
            except socket.timeout:
                print 'Socket timeout, loop and try recv() again'
                # traceback.print_exc()
                continue

            except:
                traceback.print_exc()
                print 'Other Socket err, exit and try creating socket again'
                # break from loop
                break
            print 'received', req
        try:
            sock.close()
        except:
            pass

do_work()
