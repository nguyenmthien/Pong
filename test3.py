import socket
import os
import subprocess
from threading import Thread
import argparse

FNULL = open(os.devnull, 'w')
IS_ON_POSIX = os.name == 'posix'
SHOW_MAC = False
USE_ARP = False

KNOWN_ARP_ERRORS_POSIX = ['-- no entry', '(incomplete)']
KNOWN_ARP_ERRORS_NT = ['No ARP Entries Found.']

def print_table(headers, table, gap=None):
    if gap is None:
        row_format = ''
        for i, h in enumerate(headers):
            gap = 0
            gap = max(gap, len(h))
            for j in table:
                gap = max(gap, len(j[i]))
            gap += 1
            row_format += "{:>%d}" % gap
        
    else:
        row_format = ("{:>%d}" % gap) * len(headers)
    print(row_format.format(*headers))
    for row in table:
        print(row_format.format(*row))

    return gap

def mac_for_ip(ip):
    if IS_ON_POSIX:
        output = subprocess.check_output(['arp', '-n', ip]).decode('ascii')
        for i in KNOWN_ARP_ERRORS_POSIX:
            if i in output:
                raise Exception()
        return output.split()[3]
    else:
        output = subprocess.check_output(['arp', '-a', ip]).decode('ascii')
        return output.splitlines()[3].split()[1].replace('-', ':')

def scan_ip_addr(ip):
    if USE_ARP:
        if IS_ON_POSIX:
            output = subprocess.check_output(['arp', '-n', ip], stderr=subprocess.STDOUT).decode('ascii')
            for i in KNOWN_ARP_ERRORS_POSIX:
                if i in output:
                    return False
            return True
        else:
            output = subprocess.check_output(['arp', '-a', ip], stderr=subprocess.STDOUT).decode('ascii')
            for i in KNOWN_ARP_ERRORS_NT:
                if i in output:
                    return False
            return True
    else:
        if IS_ON_POSIX:
            return not subprocess.call(['ping', '-c', '1', '-t', '1', ip], stdout=FNULL, stderr=subprocess.STDOUT)
        else:
            return not subprocess.call(['ping', '-n', '1', '-w', '1000', ip], stdout=FNULL, stderr=subprocess.STDOUT)
        
def ip_thread(ip, ips):
    if scan_ip_addr(ip):
        try:
            host, _, _ = socket.gethostbyaddr(ip)
        except socket.herror:
            host = ''
        
        res = [ip, host]
        if SHOW_MAC:
            try:
                mac_addr = mac_for_ip(ip)
            except:
                mac_addr = ''
            res.append(mac_addr)
        ips.append(res)


def main(ips):
    all_threads = []
    accepted_ips = []
    for ip_base in ips:
        p1, p2, p3, p4 = [[int(y) for y in x.split('-')] for x in ip_base.split('.')]
        for p in (p1, p2, p3, p4):
            if len(p) == 1:
                p.append(p[0]+1)
            else:
                p[1] += 1
        
        for i in range(p1[0], p1[1]):
            for j in range(p2[0], p2[1]):
                for k in range(p3[0], p3[1]):
                    for x in range(p4[0], p4[1]):
                        temp = Thread(target=ip_thread, args=(f'{i}.{j}.{k}.{x}',accepted_ips))
                        all_threads.append(temp)
                        temp.start()
    while True:
        for i in all_threads:
            if i.is_alive():
                break
        else:
            break
    headers = ['IP', 'HOST']
    if SHOW_MAC:
        headers.append('MAC')
    print_table(headers, accepted_ips)

def run():
    parser = argparse.ArgumentParser(description='Scan all ip addresses withing a given range')
    parser.add_argument('ip_ranges', metavar='ip range', type=str, nargs='*', default=[],
                    help='a range of ips to scan, if none is given the local net will be used')
    parser.add_argument('-m', '--mac', dest='show_mac', action='store_const',
                    const=True, default=False,
                    help='if used, the table will show the mac address of the scanned devices')
    parser.add_argument('-a', '--arp', dest='use_arp', action='store_const',
                    const=True, default=False,
                    help='if used, the request sent will be an arp request (otherwise a ping request)')
    args = parser.parse_args()
    SHOW_MAC = args.show_mac
    USE_ARP = args.use_arp
    ip_base = args.ip_ranges
    if len(ip_base) == 0:
        if IS_ON_POSIX:
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
                                   
    main(ip_base)

run()
