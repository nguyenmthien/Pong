"""Networking functionalities"""
import json
import socket
import assets

LOCAL_IP = socket.gethostbyname(socket.gethostname())
PORT_SERVER = 2033
PORT_CLIENT = 2056


class Networking:
    """Networking default class"""
    def __init__(self):
        self.reply = ""
        self.is_game_running = False
        self.is_binded = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.client_address = None

    def init_server(self):
        """Initialize socket in server mode"""
        self.socket.bind((LOCAL_IP, PORT_SERVER))
        self.is_binded = True
        print(f"Binded a TCP socket to {LOCAL_IP}:{PORT_SERVER}")
        self.socket.listen()
        print("waiting for connection")

    def init_client(self):
        """Initialize socket in client mode"""
        self.socket.bind((LOCAL_IP, PORT_CLIENT))
        self.is_binded = True
        print(f"Binded a TCP socket to {LOCAL_IP}:{PORT_CLIENT}")

    def connect_to_sever(self, ip_address):
        """Connect client to server, given IP address"""
        self.socket.connect((ip_address, PORT_SERVER))
        print(f"Conneted to server at {ip_address}:{PORT_SERVER}")
        self.is_game_running = True

    def wait_for_client(self):
        """Wait and confirm the client"""
        self.client_socket, self.client_address = self.socket.accept()
        self.client_socket.settimeout(0.5/assets.FPS)
        print(f"Conneted to client at {self.client_address}")
        print(self.client_socket)
        self.is_game_running = True

    def send_coordinates(self, asset_class: assets.Assets):
        """Send coordinates from asset_class to client"""
        binary = dict_to_binary(asset_class.get_coordinates())
        try:
            self.client_socket.send(str.encode(binary))
        except AttributeError:
            pass

    def receive_coordinates(self, asset_class: assets.Assets):
        """Use in client, recive data from server and decode it"""
        binary = self.socket.recv(2048)  # allow receiving 2048 bits data
        binary_decoded = binary.decode("utf-8")  # utf-8 encoding
        if not binary:  # if sending incompleted data
            print("disconnected")
        else:
            translated_binary = binary_to_dict(binary_decoded)
            print(f"Recieved: {translated_binary}")
            if translated_binary:
                asset_class.set_coordinates(translated_binary)

    def send_controls(self, asset_class: assets.Assets):
        """Use in client, send control to server"""
        control = asset_class.get_opponent_speed()
        self.socket.send(str(control).encode('utf-8'))

    def recieve_controls(self, asset_class: assets.Assets):
        """Use in server, recieve control from client"""
        try:
            control = self.client_socket.recv(8)
            control = control.decode('utf-8')
            if control is False:  # if sending incompleted data
                print("disconnected")
            else:
                asset_class.set_opponent_speed(int(control))
                print(f"Recieved: {control}")
        except socket.timeout:
            pass

def binary_to_dict(binary):
    """translate binary to dictionary"""
    jsn = ''.join(chr(int(x, 2)) for x in binary.split())
    try:
        return json.loads(jsn)
    except json.decoder.JSONDecodeError:
        return False

def dict_to_binary(dictionary):
    """Translate dictionary to binary"""
    string = json.dumps(dictionary)
    binary = ' '.join(format(ord(letter), 'b') for letter in string)
    return binary


if __name__ == "__main__":
    pass
