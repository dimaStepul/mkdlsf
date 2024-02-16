import requests
import gzip
import socket


def check_sites(filename, num_sites):
    with open(filename, "r") as file:
        sites = [next(file).strip() for x in range(num_sites)]

    for site in sites:
        try:
            response = requests.get(site, timeout=5)
            print(f"Site {site} is accessible.")
        except requests.exceptions.RequestException as err:
            print(f"Site {site} is not accessible. Error: {err}")


# check_sites('BlockingListLatest.txt', 10)


def send_get_request(host, port=80, path="http://"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    try:
        s.connect((host, port))
        request = f"GET {path} HTTP/1.0\r\n"
        request += f"Host: {host}\r\n"
        request += "Accept-Encoding: gzip, deflate, br\r\n"
        request += "Connection: close\r\n\r\n"
        s.sendall(request.encode())

        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data

        if "Content-Encoding: gzip" in response.decode():
            response = gzip.decompress(response)
        response_str = response.decode()

        if "HTTP/1.0 301" in response_str or "HTTP/1.0 302" in response_str:
            new_location = response_str.split("Location: ")[1].split("\r\n")[0]
            send_get_request(host, port, new_location)
        else:
            print(response_str)

    except socket.error as e:
        print(f"Ошибка при отправке запроса: {e}")

    finally:
        s.close()


# headers = {

# }

# response = requests.get('http://1xbet.gr', headers=headers)

# print(response.text)
send_get_request("example.org", 80, "/")
