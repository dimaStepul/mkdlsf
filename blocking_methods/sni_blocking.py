import socket
import ssl


def check_sni_blocking(target_sni, unrelated_sni):
    unrelated_server = ("example.com", 443)

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    sock = socket.create_connection(unrelated_server)
    sock = context.wrap_socket(sock, server_hostname=target_sni)
    try:
        sock.recv(1024)
    except ssl.SSLError:
        target_blocked = True
    else:
        target_blocked = False
    sock.close()

    sock = socket.create_connection(unrelated_server)
    sock = context.wrap_socket(sock, server_hostname=unrelated_sni)
    try:
        sock.recv(1024)
    except ssl.SSLError:
        unrelated_blocked = True
    else:
        unrelated_blocked = False
    sock.close()

    if target_blocked and not unrelated_blocked:
        print(f"There is probably SNI-based blocking on {target_sni}")
    else:
        print(f"There is probably no SNI-based blocking on {target_sni}")


check_sni_blocking("blocked.com", "ok.com")


import http.client


def check_host_header_blocking(target_host, unrelated_host):
    unrelated_server = "example.com"

    conn = http.client.HTTPConnection(unrelated_server)
    conn.putrequest("GET", "/", headers={"Host": target_host})
    try:
        conn.getresponse()
        target_blocked = False
    except http.client.RemoteDisconnected:
        target_blocked = True
    conn.close()

    conn = http.client.HTTPConnection(unrelated_server)
    conn.putrequest("GET", "/", headers={"Host": unrelated_host})
    try:
        conn.getresponse()
        unrelated_blocked = False
    except http.client.RemoteDisconnected:
        unrelated_blocked = True
    conn.close()

    if target_blocked and not unrelated_blocked:
        print(f"There is probably Host-header-based blocking on {target_host}")
    else:
        print(f"There is probably no Host-header-based blocking on {target_host}")


check_host_header_blocking("blocked.com", "ok.com")
