import sys
import socket
from scapy.all import *
from scapy.layers.inet import IP, ICMP


def get_domain(ip):
    try:
        domain = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        domain = ip
    return domain

def traceroute(destination, max_hops=30):
    ttl = 1
    while True:
        packet = IP(dst=destination, ttl=ttl) / ICMP()
        reply = sr1(packet, verbose=0, timeout=5)
        if reply is None:
            print(f"{ttl}: *")
        elif reply.src == destination:
            print(f"{ttl}: {get_domain(reply.src)} (Destination reached)")
            break
        else:
            print(f"{ttl}: {get_domain(reply.src)}")
        ttl += 1
        if ttl > max_hops:
            print("Maximum number of hops reached.")
            break


traceroute("rosguard.gov.ru")
