import json
import socket
import threading
import assets


class Networking:
    """Networking default class"""
    def __init__(self):
        self.LOCAL_IP = socket.gethostbyname(socket.gethostname())
        self.reply = ""
        self.PORT_SERVER = 2033
        self.PORT_CLIENT = 2056
        self.is_game_running = False
        self.is_binded = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def init_server(self):
        """Initialize socket in server mode"""
        self.socket.bind((self.LOCAL_IP, self.PORT_SERVER))
        self.is_binded = True
        print(f"Binded a TCP socket to {self.LOCAL_IP}:{self.PORT_SERVER}!")
        self.socket.listen(1)
        print("waiting for connection")

    def init_client(self):
        self.socket.bind((self.LOCAL_IP, self.PORT_CLIENT))
        self.is_binded = True
        print(f"Binded a TCP socket to {self.LOCAL_IP}:{self.PORT_SERVER}!")

    def connect_to_sever(self, IP):
        """Connect client to server, given IP address"""
        self.socket.connect((IP, self.PORT_SERVER))
        print(f"Conneted to server at {IP}")
        self.is_game_running = True

    def wait_for_client(self):
        """Wait and confirm the client"""
        self.client_socket, self.client_address = self.s.accept()
        print(f"Conneted to client at {self.client_address}")
        self.is_game_running = True

    def send_coordinates(self, asset_class: assets.Asset):
        """Send coordinates from asset_class to client"""
        self.binary = self.dict_to_binary(asset_class.get_cooridnates())
        self.client_socket.send(str.encode(self.binary))

    def receive_coordinates(self, asset_class: assets.Assets):
        """Use in client, recive data from server and decode it"""
        binary = self.socket.recv(2048)  # allow receiving 2048 bits data
        binary_decoded = self.data.decode("utf-8")  # utf-8 encoding
        if not self.data:  # if sending incompleted data
            print("disconnected")
        else:
            translated_binary = self.binary_to_dict(self, binary_decoded)
            asset_class.set_coordinates(translated_binary)
            print(f"Recieved: {translated_binary}")

    def send_controls(self, asset_class: assets.Assets):
        """Use in client, send control to server"""
        pass  # use getter

    def recieve_controls(self, asset_class: assets.Assets):
        """Use in server, recieve control from client"""
        pass  # use setter

    def binary_to_dict(self, binary):
        """translate binary to dictionary"""
        jsn = ''.join(chr(int(x, 2)) for x in binary.split())
        return json.loads(jsn)

    def dict_to_binary(self, dict):
        """Translate dictionary to binary"""
        str = json.dumps(dict)
        self.binary = ' '.join(format(ord(letter), 'b') for letter in str)
        return self.binary


if __name__ == "__main__":
    pass
