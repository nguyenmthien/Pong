import socket
import assets
import threading
import json

Host = socket.gethostbyname(socket.gethostname())
reply = ""
Port = 2033
Port_client = 2056
Is_game_running = False
Check_bind = False

ASSETS = assets.Assets


class Server:
    def init_server(self):
        """server initialize"""
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
        """client threading function"""
        # connect.send(str.encode("connected"))
        self.data = clientsocket.recv(2048)  # allow receiving 2048 bits data
        self.reply = self.data.decode("utf-8")  # utf-8 encoding
        if not self.data:  # if sending incompleted data
            print("disconnected")
        else:
            self.translated_binary = Server.binary_to_dict(self, self.reply)
            ASSETS.set_cooridnates(**(self.translated_binary))
            print("received:", self.reply)
            print("translated:", self.translated_binary)
        """
        clientsocket.sendall(str.encode(self.reply))
        # send reply back to client
        """
    def send_client(self):
        """client handle"""
        self.clientsocket, self.address = self.s.accept()
        print("client's address:", self.address)
        # print out client's address
        # self.send_coordinates = assets.Assets.set_cooridnates(self, Server.translated_binary)
        self.clientsocket.send("from server: speaking".encode())
        # self.clientsocket.send(self.send_coordinates.encode())
        # send data to client

        threading.Thread(target=self.threaded_client,
                         args=(self.clientsocket, )).start()
        # start new thread after sending message to client

    def binary_to_dict(self, binary):
        """translate binary to dictionary"""
        jsn = ''.join(chr(int(x, 2)) for x in binary.split())
        self.d = json.loads(jsn)
        return self.d


class Client:
    def __init__(self):
        """client initialize"""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 2033
        self.address = (self.host, self.port)
        self.id = self.connect()

    def dict_to_binary(self, dict):
        """Translate dictionary to binary"""
        str = json.dumps(dict)
        self.binary = ' '.join(format(ord(letter), 'b') for letter in str)
        return self.binary

    def connect(self):
        """Connect client to server"""
        global Is_game_running
        Is_game_running = True
        self.client.connect(self.address)
        print("is game running", Is_game_running)
        return self.client.recv(2048).decode()

    def send(self):
        """Send data to server"""
        try:
            self.data = ASSETS.get_cooridnates()
            self.binary = Client.dict_to_binary(self, self.data)
            self.client.send(str.encode(self.binary))
            # send objects' coordinates to server
            """
            reply = self.client.recv(2048).decode()
            return reply
            """
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
        SERVER.send_client()
