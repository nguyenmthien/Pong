"""Networking functionalities"""
import ipaddress
import json
import os
import select
import socket
import subprocess
import threading
import assets

# This is the local IP addr constant. Not tested on os =/= NT
LOCAL_IP = socket.gethostbyname(socket.gethostname())

# These ports is going to be used by the main server and client in game,
# but not the only ports used. These ports are choosed to incollide with
# Sid Meier's Civilization IV network multiplayer ports.
PORT_SERVER = 2033
PORT_CLIENT = 2056

# Two German quotes used in the process of validate the legitimate
# Pong server. The use of German is to avoid false positive.
# Umlauts are not a problem, since they will be encode with utf-8.
RITUAL_STR_SERVER = "Jeder nach seinen Fähigkeiten, jedem nach seinen Bedürfnissen!"
RITUAL_STR_CLIENT = "Proletarier aller Länder, vereinigt Euch!"

# Number of maximum timeout allowed for the game
# here we set it as 1.5 s
TIMEOUT_COUNT_MAX = int(3*assets.FPS)

IS_ON_POSIX = os.name == 'posix'


class Networking:
    """Networking default class"""
    def __init__(self):
        # sockets and tools
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.client_address = None
        self.socket_list = [self.socket]
        # result container
        self.ip_result = {
            "timeout": [],
            "found":   [],
            "invalid": [],
            "notfound":[],
        }
        # progress flags
        self.flag = {
            "is_game_running" : False,
            "is_binded"       : False,
            "is_scanning"     : False,
        }

        self.timeout_count = 0

    def init_server(self):
        """Initialize socket in server mode"""
        try:
            self.socket.bind((LOCAL_IP, PORT_SERVER))
        except (ConnectionRefusedError, OSError):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((LOCAL_IP, PORT_SERVER))
        self.flag["is_binded"] = True
        self.socket.setblocking(0)
        self.socket_list = [self.socket]
        print(f"Binded a TCP socket to {LOCAL_IP}:{PORT_SERVER}")
        self.socket.listen()
        print("waiting for connection")

    def wait_for_client(self):
        """Wait and confirm the client"""
        # We use select to categorize ready to read sockets form socket_list, then
        # loop through every one of them to perform the server connect ritual.
        # This instruction is blocking, consider an unblocking solution using threading
        ready_to_read, _, _ = select.select(self.socket_list, [], [])
        for notified_socket in ready_to_read:

            # The server connect ritual is to send RITUAL_STR_SERVER for every new connection
            # then wait for the return string. The game will start if the client send
            # RITUAL_STR_CLIENT, and the server will disconnect with the client if the client
            # send None

            # If our server socket is ready to read, that's mean
            # there is a new connection.

            if notified_socket == self.socket:
                self.client_socket, self.client_address = self.socket.accept()
                self.client_socket.settimeout(10/assets.FPS)
                self.client_socket.send(RITUAL_STR_SERVER.encode('utf-8'))
                try:
                    return_str = self.client_socket.recv(1024).decode('utf-8')
                except OSError as msg:
                    print(f"{msg} at wait_for_client")
                    return
                if return_str == RITUAL_STR_CLIENT:
                    print(f"Conneted to client at {self.client_address}")
                    self.client_socket.settimeout(0.5/assets.FPS)
                    self.flag["is_game_running"] = True
                    return
                if return_str is None:
                    print(f"Detected client at {self.client_address}")
                    return

    def init_client(self):
        """Initialize socket in client mode"""
        try:
            self.socket.bind((LOCAL_IP, PORT_CLIENT))
        except OSError:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((LOCAL_IP, PORT_CLIENT))
        finally:
            self.socket.settimeout(10/assets.FPS)
            self.flag["is_binded"] = True
        print(f"Binded a TCP socket to {LOCAL_IP}:{PORT_CLIENT}")

    def scan_for_server(self, ui_obj: assets.UserInterface):
        """Scan for available IPs and pass it to self.server_list"""

        # We use the IP scanner to find the list of possible host,
        # then loop through every one of them to find the pong host.
        # Note that this config use threading to speed up the search
        # process, hence we will create a lot of throwaway socket
        # in the loop

        self.flag['is_scanning'] = True
        self.ip_result['timeout'] = []
        self.ip_result['invalid'] = []
        self.ip_result['notfound'] = []
        self.ip_result['found'] = []

        ui_obj.choice = 0

        host_list = get_ip_base()
        # print(f"Found these hosts on the local network:")
        # print(host_list)
        threads = []
        for ip_list in host_list:
            # Due to the format of the ip_base: [[ip_list1], [ip_list2], ...], 
            # we now loop twice to find the ip, then pass it for validation

            for ip_addr in ip_list:
                thrd = threading.Thread(target=self.find_server_ritual,
                                        args=[ip_addr])
                thrd.start()
                threads.append(thrd)

        for thread in threads:
            thread.join()
        print(f"Scan results (timeout IPs are ommited):")
        #print(f"    Timeout: {self.ip_result['timeout']}")
        print(f"    Not found: {self.ip_result['notfound']}")
        print(f"    Invalid: {self.ip_result['invalid']}")
        print(f"    Found: {self.ip_result['found']}")
        self.flag['is_scanning'] = False
        return

    def find_server_ritual(self, ip_addr):
        """Ritual to find if the host is a legitimate pong server"""

        # The client ritual is to try to connect to the server, then
        # recieve a package. If the package is RITUAL_STR_SERVER
        # then the ip_addr is valid. If not, or we cannot connect, then the
        # ip_addr is invalid

        try:
            scan_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scan_sock.settimeout(2)
            scan_sock.connect((ip_addr, PORT_SERVER))
        except ConnectionRefusedError:
            self.ip_result['notfound'].append(ip_addr)
            return
        except socket.timeout:
            self.ip_result['timeout'].append(ip_addr)
            return
        else:
            ritual = scan_sock.recv(1024).decode('utf-8')
            scan_sock.close()

            if ritual == RITUAL_STR_SERVER:
                self.ip_result['found'].append(ip_addr)
                return

            self.ip_result['invalid'].append(ip_addr)
            return

    def connect_to_sever(self, ip_address):
        """Connect client to server, given IP address"""
        try:
            self.socket.connect((ip_address, PORT_SERVER))
        except WindowsError as err:
            print(f"{err.winerror} at connect_to_server")
            if err.winerror != 10048:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.bind((LOCAL_IP, PORT_CLIENT))
                self.socket.connect((ip_address, PORT_SERVER))
        except socket.timeout:
            pass
        finally:
            self.socket.recv(1024)
            self.socket.send(RITUAL_STR_CLIENT.encode('utf-8'))
            print(f"Conneted to server at {ip_address}:{PORT_SERVER}")
            self.flag['is_game_running'] = True
            self.socket.settimeout(0.7/assets.FPS)

    def send_coordinates(self, assets_obj: assets.Assets, ui_obj: assets.UserInterface):
        """Send coordinates from assets_obj to client"""
        binary = dict_to_binary(assets_obj.get_coordinates())
        try:
            self.client_socket.send(str.encode(binary))
        except AttributeError as msg:
            print(f"{msg} at send_coordinates")
        except socket.timeout as msg:
            print(f"{msg} at send_coordinates")
            self.timeout_count += 1
            if self.timeout_count >= TIMEOUT_COUNT_MAX:
                print(f"End hosting due to timeout_count={self.timeout_count}")
                self.end_hosting(assets_obj, ui_obj)
        except (ConnectionAbortedError,
                ConnectionRefusedError,
                ConnectionResetError) as msg:
            print(f"{msg} at send_coordinates")
            self.end_hosting(assets_obj, ui_obj)
        else:
            self.timeout_count = 0

    def receive_coordinates(self, assets_obj: assets.Assets, ui_obj: assets.UserInterface):
        """Use in client, recive data from server and decode it"""
        try:
            binary = self.socket.recv(2048)  # allow receiving 2048 bits data
            if not binary:  # if sending incompleted data
                print("disconnected")
                self.network_disconnect(assets_obj, ui_obj)
                return
            binary_decoded = binary.decode("utf-8")  # utf-8 encoding
            translated_binary = binary_to_dict(binary_decoded)
            # print(f"Recieved: {translated_binary}")
            if translated_binary:
                assets_obj.set_coordinates(translated_binary)
                self.timeout_count = 0
        except OSError as msg:
            self.timeout_count += 1
            if self.timeout_count >= TIMEOUT_COUNT_MAX:
                print(f"Disconnect due to timeout count = {self.timeout_count}")
                self.network_disconnect(assets_obj, ui_obj)
            print(f"{msg}: at receive_coordinates, count: {self.timeout_count}")


    def send_controls(self, assets_obj: assets.Assets, ui_obj: assets.UserInterface):
        """Use in client, send control to server"""
        control = assets_obj.get_opponent_speed()
        try:
            self.socket.send(str(control).encode('utf-8'))
        except (ConnectionAbortedError, OSError):
            self.network_disconnect(assets_obj, ui_obj)

    def recieve_controls(self, assets_obj: assets.Assets, ui_obj: assets.UserInterface):
        """Use in server, recieve control from client"""
        # TODO: change to select
        #       add logic branch to avoid set speed to 66 or -66
        try:
            control = self.client_socket.recv(10)
            control = control.decode('utf-8')
            print(f"Recieved: {control}")
            if control is None:  # if sending incompleted data
                print("disconnected")
                self.network_disconnect(assets_obj, ui_obj)
            else:
                assets_obj.set_opponent_speed(int(control))
        except socket.timeout:
            pass
        except ValueError as msg:
            print(f"{msg} at recieve_controls")
        except OSError as msg:
            print(f"{msg} at recieve_controls")

    def end_hosting(self, assets_obj: assets.Assets, ui_obj: assets.UserInterface):
        """Use in server to end multiplayer mode"""
        self.flag['is_binded'] = False
        self.flag['is_game_running'] = False
        assets_obj.reset()
        ui_obj.current_menu = "TITLE SCREEN"
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except (socket.error, OSError, ValueError) as msg:
            print(f"{msg} at end_hosting")
        self.socket.close()

    def network_disconnect(self, assets_obj: assets.Assets, ui_obj: assets.UserInterface):
        """Use in client to end multiplayer mode"""
        self.flag['is_binded'] = False
        self.flag['is_game_running'] = False
        assets_obj.reset()
        ui_obj.current_menu = "TITLE SCREEN"
        try:
            self.socket.close()
        except (socket.error, OSError, ValueError) as msg:
            print(f"{msg} at network_disconnect")


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


def ip2bin(ip_addr):
    """Convert IP address to binary"""
    octets = map(int, ip_addr.split('/')[0].split('.'))
    binary = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets)
    range_bin = int(ip_addr.split('/')[1]) if '/' in ip_addr else None
    return binary[:range_bin] if range_bin else binary


def get_prefix(binary):
    """Get the prefix of Subnet Mask"""
    prefix_count = 0
    for i in binary:
        if i == '1':
            prefix_count += 1
    return prefix_count


def get_ip_base():
    """Get list of IP in Network"""
    ip_addr = []
    subnet_mask = []
    if len(ip_addr) == 0:
        if IS_ON_POSIX:
            broadcast = []
            box = []
            ifconfig = subprocess.check_output('ifconfig').decode('ascii').splitlines()
            for i in ifconfig:
                if 'broadcast' in i:
                    broadcast = i.split('broadcast')[1].strip()
                    ip_addr.append('.'.join(broadcast.split('.')[:-1]) + '.0')
                if 'Mask' in i:
                    box = i.split()[-1].strip()
                    subnet_mask.append(box)
        else:
            ipconfig = subprocess.check_output('ipconfig').decode('ascii').splitlines()
            for i in ipconfig:
                if 'IPv4 Address' in i:
                    broadcast = i.split()[-1].strip()
                    ip_addr.append('.'.join(broadcast.split('.')[:-1]) + '.0')
                if 'Subnet Mask' in i:
                    box = i.split()[-1].strip()
                    subnet_mask.append(box)

    ip_base = []
    for i, subnet in enumerate(subnet_mask):
        prefixlen = str(get_prefix(ip2bin(subnet)))
        ip_add = ip_addr[i]
        ip_base.append(ip_add + '/' + prefixlen)

    j = 0
    list_ip = []
    for i, _ in enumerate(ip_base):
        list_ip.append(list(ipaddress.ip_network(ip_base[j]).hosts()))
        j = j+1

    for i, ip_list in enumerate(list_ip):                   #Convert ip in list_ip to string
        for j, addr in enumerate(ip_list):
            list_ip[i][j] = str(addr)

    return list_ip


if __name__ == "__main__":
    # all of these is only used for testing only.
    import time
    import pygame
    def ui_thread():
        """Thread for threading"""
        while NET.flag["is_scanning"]:
            UI.wait_for_search(ASSETS)
            pygame.event.get()
    def net_thread():
        """Thread for threading"""
        NET.scan_for_server(UI)
    ASSETS = assets.Assets()
    UI = assets.UserInterface()
    NET = Networking()
    UI_THR = threading.Thread(target=ui_thread, args=[])
    NET_THR = threading.Thread(target=net_thread, args=[])
    print(f"created threads successfully!")
    T1 = time.time()
    UI_THR.start()
    NET_THR.start()
    NET_THR.join()
    UI_THR.join()
    T2 = time.time()
    UI.choose_server(ASSETS, NET.ip_result['found'])
    print(f"Scanning time: {T2-T1} s")
    time.sleep(5)
