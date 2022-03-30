import socket
#threading은 high level에서 멀티 쓰레드를 가능하게 하고 tread는 low level에서 멀티 쓰레드를 가능하게 한다.
import threading

#ipconfig으로 로컬 호스트 알 수 있음.
HOST = '127.0.0.1'
PORT = 9090


#socket(): 소켓을 생성.
#bind(): ip와 port를 설정함.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


#대기하고 있다가 클라이언트의 연결 요청이 들어오면 몇 개의 클라이언트를 대기 시킬지 결정.
server.listen()


#클라이언트 목록
#각 클라이언트의 닉네임 목록
clients = []
nicknames = []


#broadcast function: 서버에 전송되는 메세지를 다른 클라이언트들도 볼 수 있게 다시 클라이언트한테 전송.
def broadcast(message):
    for client in clients:
        client.send(message)


#receive function: 새로운 클라이언트를 연결해줌.
#accept(): 서버를 향한 클라이언트의 연결 요청을 수락함.
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        #send(): 연결된 서버나 클라이언트로 데이터를 전송함.
        client.send("NICK".encode('utf-8'))
        #recv(): send()가 보내온 데이터를 수신함.
        nickname = client.recv(1024)

        #닉네임 리스트에 입력 받은 닉네임 추가
        nicknames.append(nickname)
        #클라이언트 리스트에 접속한 클라이언트 추가
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))
        
        #쓰레드(thread)가 handle()를 실행할 것이고 handle()의 return한 결과가 target에 지정하기 때문에 handle()의 입력 매개변수는 args()에 작성하면 된다.
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