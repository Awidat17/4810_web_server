import socket
import threading
import time

def talk():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(5)
    while True:
        clientsocket,address = s.accept()
        #print(f"Connection from{address}has been established!")
        clientsocket.send(bytes("90:Working","utf-8"))

