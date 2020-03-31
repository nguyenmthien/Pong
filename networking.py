import socket
from _thread import *

host = "192.168.1.5"  # local IPv4 address
reply = ""
port = 2033
clients = 2
clients_count = 0


class Server():
    def init_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket declaration
        self.bind = self.s.bind((host, port))  # bind host and port
        print("socket binded to port", port)

        self.s.listen(clients)  # allow upto 2 clients connection
        print("waiting for connection")

    def threaded_client(self, connect):
        """Threaded function"""
        # connect.send(str.encode("connected"))
        self.data = connect.recv(2048)  # allow receiving 2048 bits data
        self.reply = self.data.decode("utf-8")  # utf-8 encoding
        if not self.data:  # if sending incompleted data
            print("disconnected")
        else:
            print("received", self.reply)
        connect.sendall(str.encode(self.reply))  # send reply back to client
        # connect.close()

    def sending_client(self):
        """connection function"""
        self.connect, self.address = self.s.accept()
        print("client's address:", self.address)
        self.clients_count += 1
        self.connect.send("from server: speaking".encode())
        # send data to client
        start_new_thread(self.threaded_client, (self.connect, ))
        # start new thread after sending message to client
        return self.clients_count


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.address)
        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as error:
            return str(error)


def send_coordinates():
    """Server send coordinates of players"""


def receive_coordinates():
    """Server receive coordinates of players"""


if __name__ == "__main__":
    SERVER = Server()
    SERVER.init_server()
    while True:
        SERVER.sending_client()
