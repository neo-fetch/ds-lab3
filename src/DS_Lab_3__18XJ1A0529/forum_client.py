import socket
import time
import os
from tqdm import tqdm
import _thread


HOST = '127.0.0.1'
PORT_S = 9090
# PORT_S = 8080

client_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_skt.connect((HOST,PORT_S)) # change HOST to the IP of the server you want to send text to

def servermsgs():
    while True:
            msg = client_skt.recv(1024).decode('utf-8')
            if not msg:
                break
            print(msg)

_thread.start_new_thread(servermsgs, ( ))
print("Enter message and the client number separated by a \':\'(For example: 2:\'message\' sends message to User2) or /quit to exit:\n")
while True:
    
    msg = input()
    msgcpy = msg
    msg=msg.encode("utf-8")
    client_skt.sendall(msg)
    if msgcpy == "/quit":
        quit()

