import socket
import ssl
import http.client
import os


class BlockingStrategy:
    def check_blocking(self, target, unrelated):
        pass


class SNIBlocking(BlockingStrategy):
    def check_blocking(self, target, unrelated):
        unrelated_server = ("example.com", 443)

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        sock = socket.create_connection(unrelated_server)
        sock = context.wrap_socket(sock, server_hostname=target)
        try:
            sock.recv(1024)
        except ssl.SSLError:
            target_blocked = True
        else:
            target_blocked = False
        sock.close()

        sock = socket.create_connection(unrelated_server)
        sock = context.wrap_socket(sock, server_hostname=unrelated)
        try:
            sock.recv(1024)
        except ssl.SSLError:
            unrelated_blocked = True
        else:
            unrelated_blocked = False
        sock.close()

        if target_blocked and not unrelated_blocked:
            print(f"There is probably SNI-based blocking on {target}")
        else:
            print(f"There is probably no SNI-based blocking on {target}")


# class HostHeaderBlocking(BlockingStrategy):
#     def check_blocking(self, target, unrelated):
#         unrelated_server = "example.com"
#
#         conn = http.client.HTTPConnection(unrelated_server)
#         conn.putrequest("GET", "/", headers={"Host": target})
#         try:
#             conn.getresponse()
#             target_blocked = False
#         except http.client.RemoteDisconnected:
#             target_blocked = True
#         conn.close()
#
#         conn = http.client.HTTPConnection(unrelated_server)
#         conn.putrequest("GET", "/", headers={"Host": unrelated})
#         try:
#             conn.getresponse()
#             unrelated_blocked = False
#         except http.client.RemoteDisconnected:
#             unrelated_blocked = True
#         conn.close()
#
#         if target_blocked and not unrelated_blocked:
#             print(f"There is probably Host-header-based blocking on {target}")
#         else:
#             print(f"There is probably no Host-header-based blocking on {target}")


class Context:
    def __init__(self, strategy: BlockingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: BlockingStrategy):
        self._strategy = strategy

    def check_blocking(self, target, unrelated):
        self._strategy.check_blocking(target, unrelated)


def check_blocking_from_file(file_path, context: Context):
    with open(file_path, "r") as file:
        websites = [line.strip() for line in file]
    for site in websites:
            context.check_blocking(site, "beb.com")
    else:
        print("Error: Invalid file or file does not exist.")
        exit(1)


def check_blocking_from_input(context: Context):
    target = input("Enter target website: ")
    unrelated = input("Enter unrelated website: ")
    context.check_blocking(target, unrelated)

def test_sites_from_file(filename):
    with open(filename, "r") as file:
        websites = [line.strip() for line in file]


context = Context(SNIBlocking())
context.check_blocking("vk.com", "example.com")