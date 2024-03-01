import argparse
import os
import socket
import ssl
import http.client


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


class DNSBlocking(BlockingStrategy):
    def check_blocking(self, target, unrelated):
        pass


class HTTPBlocking(BlockingStrategy):
    def check_blocking(self, target, unrelated):
        pass


class CensorshipChecker:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="cypriot censorship cheker",
            description="What the program does",
            epilog="Text at the bottom of help",
        )

        self.parser.add_argument(
            "-s", "--site", type=str, help="Website domain to check"
        )
        self.parser.add_argument(
            "-p", "--port", type=int, help="Port to use for the check"
        )
        self.parser.add_argument(
            "-f", "--file", type=str, help="File with a list of websites to check"
        )
        self.parser.add_argument(
            "-b",
            "--block",
            type=str,
            choices=["sni_blocking", "dns", "http"],
            help="Type of blocking to bypass",
        )

        self.args = self.parser.parse_args()

    def check_args(self):
        if self.args.site:
            self.site = self.args.site
        else:
            print("Error: No website domain provided.")
            exit(1)

        if self.args.port and isinstance(self.args.port, int):
            self.port = self.args.port
        else:
            print("Error: Invalid or no port provided.")
            exit(1)

        if self.args.file and os.path.isfile(self.args.file):
            self.file = self.args.file
        else:
            print("Error: Invalid file or file does not exist.")
            exit(1)

        if self.args.block:
            self.block = self.args.block
        else:
            print("Error: No blocking type provided.")
            exit(1)

    def run(self):
        if self.block == "sni_blocking":
            strategy = SNIBlocking()
        elif self.block == "dns":
            strategy = DNSBlocking()
        else:
            strategy = HTTPBlocking()

        if self.file:
            with open(self.file, "r") as file:
                for line in file:
                    target, unrelated = line.strip().split(",")
                    strategy.check_blocking(target, unrelated)
        else:
            strategy.check_blocking(self.site, self.port)


checker = CensorshipChecker()
checker.check_args()
checker.run()


if __name__ == "__main__":
    checker = CensorshipChecker()
    checker.check_args()
    checker.run()
