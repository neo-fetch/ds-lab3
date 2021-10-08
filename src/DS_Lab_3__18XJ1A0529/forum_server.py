import socket
import time
import os
from tqdm import tqdm
import _thread


HOST = '127.0.0.1'
PORT_R = 9090
threads = {"num":0}
usrs = []
connections = {}
# PORT_S = 8080
    

def users(connection, user,num):
    for cn in connections.keys():    
        connections[cn].sendall(f"{user} has joined.\n    Currently online:{[usr for usr in usrs]}".encode('utf-8'))
    usr_send = ''
    message_send = ''
    while True:
        data = connection.recv(1024).decode('utf-8')
        if not data: break
        if data == "/quit":
            del connections[user]
            usrs.remove(user)
            for cn in connections.keys():    
                connections[cn].sendall(f"{user} has left the chat.\n    Currently online:{[usr for usr in usrs]}".encode('utf-8'))
        if data == "/update":
            connection.sendall(f"Currently online:{[usr for usr in usrs]}".encode('utf-8'))
        data = data.split(':')
        usr_send = "User" + data[0]
        message_send = f"User{num}: {data[1]}".encode('utf-8')
        connections[usr_send].sendall(message_send)
        print(f"{message_send.decode('utf-8')} \n>")

    connection.close()

    

serv_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_skt.bind((HOST, PORT_R))
serv_skt.listen(5)
print("waiting for a client...")

while True:
    connection, address = serv_skt.accept()
    print(f"{address} is now connected at {HOST}")
    user = "User" + str(threads["num"])
    usrs.append(user)
    connections[user] = connection
    _thread.start_new_thread(users, (connection,user,threads["num"], ))
    threads["num"] += 1
    print(f"Total threads: {threads['num']}")

serv_skt.close()