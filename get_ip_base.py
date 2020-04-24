import os
import subprocess
import ipaddress

FNULL = open(os.devnull, 'w')
IS_ON_POSIX = os.name == 'posix'
SHOW_MAC = False
USE_ARP = False

KNOWN_ARP_ERRORS_POSIX = ['-- no entry', '(incomplete)']
KNOWN_ARP_ERRORS_NT = ['No ARP Entries Found.']

def get_ip_base():
    """Find IP base for scanning"""
    ip_base = []
    if len(ip_base) == 0:
        if IS_ON_POSIX:
            broadcast = []
            ifconfig = subprocess.check_output('ifconfig').decode('ascii').splitlines()
            for i in ifconfig:
                if 'broadcast' in i:
                    broadcast = i.split('broadcast')[1].strip()
                    ip_base.append('.'.join(broadcast.split('.')[:-1]) + '.0/24')
        else:
            ipconfig = subprocess.check_output('ipconfig').decode('ascii').splitlines()
            for i in ipconfig:
                if 'IPv4 Address' in i:
                    broadcast = i.split()[-1].strip()
                    ip_base.append('.'.join(broadcast.split('.')[:-1]) + '.0/24')

    j=0
    list_ip = []
    for i in range(len(ip_base)):
        list_ip.append(list(ipaddress.ip_network(ip_base[j]).hosts()))
        j = j+1
    return list_ip
    

if __name__ == '__main__':
    print(get_ip_base())