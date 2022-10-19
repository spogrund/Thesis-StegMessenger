import socket
import threading

HOST = '127.0.0.1'
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []
keys = []

print(f"listening on {HOST}:{PORT}")


def sendToRec(msg, name):
    for client in clients:
        if name == names[clients.index(client)]:
            client.send(msg)

def sendToAll(msg):
    for client in clients:
        client.send(msg)


def rcvMsg(client):
    while True:


        try:
            msg = client.recv(1024)
            msg = msg.decode()
            print(msg)

            #if "new receiver" in msg:
             #   sendToAll(f"you are now in a chat with: {names[clients.index(client)]}\n".encode(), msg[msg.find(",")+1:])

            if msg[msg.find(": ")+1:] == "q":
                server.close()
            elif "LON" in msg:
                msg = f"LON: {str(names)}".encode()
                print(msg)
                client.send(msg)
            else:
                receiver_name = msg[:msg.find(',')]
                #sendToRec(msg.encode(), receiver_name)
                sendToAll(msg.encode())
                #client.send(msg[msg.find(",")+1:].encode())
        except:
            print("error: ")
            clients.remove(client)
            names.pop(clients.index(client))

            break

def newClient():
    while True:
        client, addr = server.accept()
        client.send("name".encode('utf-8'))
        nickname = client.recv(1024)

        clients.append(client)
        names.append(nickname.decode())

        print(f"{nickname.decode()} has connected to the server")
        msg = f"LON: {str(names)}".encode()
        for client in clients:
            client.send(msg)
        thread = threading.Thread(target=rcvMsg, args=(client,))
        thread.start()
newClient()