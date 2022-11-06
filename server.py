"""
PGRSAM001
EEE4022S
Final year project
Server module
"""
import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#binding a socket to a local port to enable communication with user sockets
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

print(f"listening on {HOST}:{PORT}")

#method to send a message to a specific user.
def sendToRec(msg, name):
    for client in clients:
        if name == names[clients.index(client)]:
            client.send(msg)

#handles what happens when the server receives a message from a user
def rcvMsg(client):
    while True:
        try:
            msg = client.recv(1024)
            msg = msg.decode()
            receiver_name = msg[:msg.find(',')]
            sender_name = msg[msg.find(',')+1: msg.find('\'')]
            msgs = msg[msg.find('\'')+1:]
            msgs = msgs[msg.find(':')+1:]
            print(msgs)
            sendToRec(msg.encode(), receiver_name)
        except:
            print("error: ")
            clients.remove(client)
            names.pop(clients.index(client))
            break
#Handles when a new user connects to the server. Updates name list and initiates the key exchange
def newClient():
    while True:
        client, addr = server.accept()
        client.send("name".encode())
        nickname = client.recv(1024).decode()
        clients.append(client)
        names.append(nickname)
        print(f"{nickname} has connected to the server")
        msg = f"LON: {str(names)}".encode()
        msg2 = f"new user:{nickname}".encode()
        for client in clients:
            client.send(msg2)
        time.sleep(1)
        for client in clients:
            client.send(msg)
        thread = threading.Thread(target=rcvMsg, args=(client,))
        thread.start()


newClient()
