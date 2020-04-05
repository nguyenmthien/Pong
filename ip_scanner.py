"""Scan IP
"""
import socket
import os
import subprocess
from threading import Thread

FNULL = open(os.devnull, 'w')
IS_ON_POSIX = os.name == 'posix'
SHOW_MAC = False
USE_ARP = False

KNOWN_ARP_ERRORS_POSIX = ['-- no entry', '(incomplete)']
KNOWN_ARP_ERRORS_NT = ['No ARP Entries Found.']

class ScanIP:
    """Class for IP Scanner"""
    def __init__(self):
        self.fnull = open(os.devnull, 'w')
        self.is_on_posix = os.name == 'posix'
        self.show_mac = False
        self.use_arp = False

        self.known_arp_errors_posix = ['-- no entry', '(incomplete)']
        self.known_arp_errors_nt = ['No ARP Entries Found.']

    def mac_for_ip(self, ip_addr):
        """Scan mac address"""
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


    def main(self, ips):
        """Return IP address and Host"""
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
                            temp = Thread(target=self.ip_thread,
                                          args=(f'{i_1}.{i_2}.{i_3}.{i_4}', accepted_ips))
                            all_threads.append(temp)
                            temp.start()
        while True:
            for i in all_threads:
                if i.is_alive():
                    break
            else:
                break
        headers = ['IP', 'HOST']
        if self.show_mac:
            headers.append('MAC')
        return accepted_ips

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

if __name__ == '__main__':
    ob = ScanIP()
    ob.main(ob.get_ip_base())