import socket
import threading

#ipconfig으로 로컬 호스트 알 수 있음.
HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []



#broadcast function: 모든 메세지를 클라이언트한테 뿌림
def broadcast(message):
    for client in clients:
        client.send(message)

#receive function: 새로운 클라이언트를 연결해줌
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")


        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)


        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))
        
        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()



#handle function: 클라이언트끼리를 연결해줌.
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


print("Server running right")
receive()