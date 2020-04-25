import os
import subprocess
import ipaddress

FNULL = open(os.devnull, 'w')
IS_ON_POSIX = os.name == 'posix'
SHOW_MAC = False
USE_ARP = False

KNOWN_ARP_ERRORS_POSIX = ['-- no entry', '(incomplete)']
KNOWN_ARP_ERRORS_NT = ['No ARP Entries Found.']

import os
import subprocess
import ipaddress

def ip2bin(ip):
    """Convert IP address to binary"""
    octets = map(int, ip.split('/')[0].split('.')) # '1.2.3.4'=>[1, 2, 3, 4]
    binary = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets)
    range = int(ip.split('/')[1]) if '/' in ip else None
    return binary[:range] if range else binary

def getPrefix(binary):
    """Get the Prefix of Subnetmask"""
    prefixCount=0
    for i in (str(binary)):
        if(i == '1'):
            prefixCount+=1
    return prefixCount

def get_ip_base():
    """Find IP base for scanning"""
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
    for i in range(len(subnet_mask)):
        prefixlen = str(getPrefix(ip2bin(subnet_mask[i])))
        ip = ip_addr[i]
        ip_base.append(ip + '/' + prefixlen)

    j=0
    list_ip = []
    for i in range(len(ip_base)):
        list_ip.append(list(ipaddress.ip_network(ip_base[j]).hosts()))
        j = j+1
        
    for i in range(len(list_ip)):                   #Convert ip in list_ip to string
        for j in range(len(list_ip[i])):
            list_ip[i][j] = str(list_ip[i][j])

    return list_ip

if __name__ == '__main__':
    print(get_ip_base())
    