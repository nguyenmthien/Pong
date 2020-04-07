"""Networking functionalities"""
import json
import os
import socket
import subprocess
import threading
import assets

LOCAL_IP = socket.gethostbyname(socket.gethostname())  # only known to work on os=NT
PORT_SERVER = 2033
PORT_CLIENT = 2056

class ScanIP:
    """Scan IP for ping-able hosts"""
    def __init__(self):
        self.fnull = open(os.devnull, 'w')
        self.is_on_posix = os.name == 'posix'
        self.show_mac = False
        self.use_arp = False

        self.known_arp_errors_posix = ['-- no entry', '(incomplete)']
        self.known_arp_errors_nt = ['No ARP Entries Found.']

    def mac_for_ip(self, ip_addr):
        """Return MAC address from parsing arp"""
        if self.is_on_posix:
            output = subprocess.check_output(['arp', '-n', ip_addr]).decode('ascii')
            for i in self.known_arp_errors_posix:
                if i in output:
                    raise Exception()
            return output.split()[3]
        else:
            output = subprocess.check_output(['arp', '-a', ip_addr]).decode('ascii')
            return output.splitlines()[3].split()[1].replace('-', ':')

    def scan_ip_addr(self, ip_addr):
        """Scan IP address using arp or ping"""
        if self.use_arp:
            if self.is_on_posix:
                output = subprocess.check_output(['arp', '-n', ip_addr],
                                                 stderr=subprocess.STDOUT).decode('ascii')
                for i in self.known_arp_errors_posix:
                    if i in output:
                        return False
                return True
            else:
                output = subprocess.check_output(['arp', '-a', ip_addr],
                                                 stderr=subprocess.STDOUT).decode('ascii')
                for i in self.known_arp_errors_nt:
                    if i in output:
                        return False
                return True
        else:
            if self.is_on_posix:
                return not subprocess.call(['ping', '-c', '1', '-t', '1', ip_addr],
                                           stdout=self.fnull,
                                           stderr=subprocess.STDOUT)
            else:
                return not subprocess.call(['ping', '-n', '1', '-w', '1000', ip_addr],
                                           stdout=self.fnull,
                                           stderr=subprocess.STDOUT)

    def ip_thread(self, ip_addr, ips):
        """Thread for multithreading"""
        if self.scan_ip_addr(ip_addr):
            try:
                host, _, _ = socket.gethostbyaddr(ip_addr)
            except socket.herror:
                host = ''
            res = [ip_addr, host]
            if self.show_mac:
                try:
                    mac_addr = mac_for_ip(ip_addr)
                except:  # pylint: disable=W0702
                    mac_addr = ''
                res.append(mac_addr)
            ips.append(res)

    def get_ip_base(self):
        """Find IP base for scanning"""
        ip_base = []
        if len(ip_base) == 0:
            if self.is_on_posix:
                broadcast = []
                ifconfig = subprocess.check_output('ifconfig').decode('ascii').splitlines()
                for i in ifconfig:
                    if 'broadcast' in i:
                        broadcast = i.split('broadcast')[1].strip()
                        ip_base.append('.'.join(broadcast.split('.')[:-1]) + '.1-254')
            else:
                ipconfig = subprocess.check_output('ipconfig').decode('ascii').splitlines()
                for i in ipconfig:
                    if 'IPv4 Address' in i:
                        broadcast = i.split()[-1].strip()
                        ip_base.append('.'.join(broadcast.split('.')[:-1]) + '.1-254')
        return ip_base

    def main(self, ips):
        """Return list of available [IP, hostname, (MAC)]"""
        all_threads = []
        accepted_ips = []
        for ip_addr in ips:
            p_1, p_2, p_3, p_4 = [[int(y) for y in x.split('-')] for x in ip_addr.split('.')]
            for p_i in (p_1, p_2, p_3, p_4):
                if len(p_i) == 1:
                    p_i.append(p_i[0]+1)
                else:
                    p_i[1] += 1

            for i_1 in range(p_1[0], p_1[1]):
                for i_2 in range(p_2[0], p_2[1]):
                    for i_3 in range(p_3[0], p_3[1]):
                        for i_4 in range(p_4[0], p_4[1]):
                            temp = threading.Thread(target=self.ip_thread,
                                                    args=(f'{i_1}.{i_2}.{i_3}.{i_4}', accepted_ips))
                            all_threads.append(temp)
                            temp.start()
        while True:
            for i in all_threads:
                if i.is_alive():
                    break
            else:
                break

        return accepted_ips


class Networking:
    """Networking default class"""
    def __init__(self):
        self.reply = ""
        self.is_game_running = False
        self.is_binded = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.client_address = None
        self.server_list = []

    def init_server(self):
        """Initialize socket in server mode"""
        self.socket.bind((LOCAL_IP, PORT_SERVER))
        self.is_binded = True
        print(f"Binded a TCP socket to {LOCAL_IP}:{PORT_SERVER}")
        self.socket.listen()
        print("waiting for connection")

    def wait_for_client(self):
        """Wait and confirm the client"""
        # TODO: change to fit with client ritual
        self.client_socket, self.client_address = self.socket.accept()
        self.client_socket.settimeout(0.5/assets.FPS)
        print(f"Conneted to client at {self.client_address}")
        print(self.client_socket)
        self.is_game_running = True

    def init_client(self):
        """Initialize socket in client mode"""
        self.socket.bind((LOCAL_IP, PORT_CLIENT))
        self.is_binded = True
        print(f"Binded a TCP socket to {LOCAL_IP}:{PORT_CLIENT}")

    def scan_for_server(self, ui_obj: assets.UserInterface, ip_scanner: ScanIP):
        """Scan for available IPs and pass it to self.server_list"""
        ui_obj.server_ip_list = []
        host_list = ip_scanner.main(ip_scanner.get_ip_base())
        for ip_list in host_list:
            if self.find_server_ritual(ip_list[0]):
                ui_obj.server_ip_list.append(ip_list[0])

    def find_server_ritual(self, ip_addr):
        """Ritual to find if the host is a legitimate pong server"""
        # TODO: add find server ritual
        return True

    def connect_to_sever(self, ip_address):
        """Connect client to server, given IP address"""
        self.socket.connect((ip_address, PORT_SERVER))
        print(f"Conneted to server at {ip_address}:{PORT_SERVER}")
        self.is_game_running = True

    def send_coordinates(self, assets_obj: assets.Assets):
        """Send coordinates from assets_obj to client"""
        binary = dict_to_binary(assets_obj.get_coordinates())
        try:
            self.client_socket.send(str.encode(binary))
        except AttributeError:
            pass

    def receive_coordinates(self, assets_obj: assets.Assets):
        """Use in client, recive data from server and decode it"""
        binary = self.socket.recv(2048)  # allow receiving 2048 bits data
        binary_decoded = binary.decode("utf-8")  # utf-8 encoding
        if not binary:  # if sending incompleted data
            print("disconnected")
        else:
            translated_binary = binary_to_dict(binary_decoded)
            print(f"Recieved: {translated_binary}")
            if translated_binary:
                assets_obj.set_coordinates(translated_binary)

    def send_controls(self, assets_obj: assets.Assets):
        """Use in client, send control to server"""
        control = assets_obj.get_opponent_speed()
        self.socket.send(str(control).encode('utf-8'))

    def recieve_controls(self, assets_obj: assets.Assets):
        """Use in server, recieve control from client"""
        try:
            control = self.client_socket.recv(5)
            control = control.decode('utf-8')
            if control is False:  # if sending incompleted data
                print("disconnected")
            else:
                assets_obj.set_opponent_speed(int(control))
                print(f"Recieved: {control}")
        except socket.timeout:
            pass
        except ValueError:
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
    import time

    SCAN_IP = ScanIP()
    T3 = time.time()
    print(SCAN_IP.main(SCAN_IP.get_ip_base()))
    T4 = time.time()
    print(T4-T3)

    ASSETS = assets.Assets()
    UI = assets.UserInterface()
    NET = Networking()
    UI.choose_server(ASSETS)
    T1 = time.time()
    NET.scan_for_server(UI, SCAN_IP)
    T2 = time.time()
    UI.choose_server(ASSETS)
    print(T2-T1)
    time.sleep(5)
