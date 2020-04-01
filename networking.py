import socket
import controls
import assets
import threading

Host = socket.gethostbyname(socket.gethostname())
reply = ""
Port = 2033
Port_client = 2056
Is_game_running = False
Check_bind = False


class Server():
    def init_server(self):
        global Check_bind
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket declaration
        self.bind = self.s.bind((Host, Port))  # bind host and port
        Check_bind = True
        print("Bind status", Check_bind)
        print("socket binded to port", Port)

        self.s.listen(1)  # allow upto 1 client connection
        print("waiting for connection")

    def threaded_client(self, clientsocket):
        # connect.send(str.encode("connected"))
        self.data = clientsocket.recv(2048)  # allow receiving 2048 bits data
        self.reply = self.data.decode("utf-8")  # utf-8 encoding
        if not self.data:  # if sending incompleted data
            print("disconnected")
        else:
            print("received", self.reply)
        clientsocket.sendall(str.encode(self.reply))
        # send reply back to client

    def sending_client(self):
        """client handle"""
        self.clientsocket, self.address = self.s.accept()
        print("client's address:", self.address)
        # print out client's address

        self.clientsocket.send("from server: speaking".encode())
        # send data to client

        threading.Thread(target=self.threaded_client,
                         args=(self.clientsocket, )).start()
        # start new thread after sending message to client


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.host = socket.gethostbyname(socket.gethostname())
        # self.port = 2033
        self.address = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        """Connect client to server"""
        global Is_game_running
        self.client.connect(self.address)
        Is_game_running = True
        print("game is running")
        return self.client.recv(2048).decode()

    def send(self, data):
        """Send data to server"""
        try:

            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as error:
            return str(error)

# client send receive
# server send receive
# create constructor for new class
# in server receive
# control from client to server sending function
# bind server and bind client, not in loop, once
# -> 1 logic variable to check whether they are binded or not


def send_coordinates():
    """Server send coordinates of players and ball"""


def receive_coordinates():
    """Server receive coordinates of players and ball"""
    # receive objects coordinate


if __name__ == "__main__":
    SERVER = Server()
    SERVER.init_server()
    while True:
        SERVER.sending_client()
