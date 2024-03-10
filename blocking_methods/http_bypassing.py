import requests
import gzip
import socket


def write_to_file(filename, data):
    with open(filename, "a") as f:
        f.write("%s\n" % data)


def _decode_bytes(input_bytes):
    return input_bytes.decode(errors="replace")


def send_request(
    host, port, data, html_file, txt_file, fragment_size=0, fragment_count=0
):
    sock = socket.create_connection((host, port), 10)
    if fragment_count:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
    try:
        for fragment in range(fragment_count):
            print("fragment", fragment)

            write_to_file(html_file, "fragment" + str(fragment))
            write_to_file(txt_file, "fragment" + str(fragment))

            sock.sendall(data[:fragment_size].encode())
            data = data[fragment_size:]
            print(data)

            write_to_file(html_file, str(data))
            write_to_file(txt_file, str(data))

        sock.sendall(data.encode())
        recvdata = sock.recv(8192)
        recv = recvdata
        recv_decoded = recv.decode()
        print(recv.decode())

        write_to_file(html_file, recv_decoded)
        write_to_file(txt_file, recv_decoded)
        while recvdata:
            recvdata = sock.recv(8192)
            recv += recvdata
    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        sock.close()
    return _decode_bytes(recv)


def configure_request_body(host, urn="/"):
    requests = {
        "extra space after  GET": {
            "data": "GET  {} HTTP/1.0\r\n".format(urn)
            + "Host: {}\r\nConnection: close\r\n\r\n".format(host),
            "fragment_size": 0,
            "fragment_count": 0,
        },
        "extra line break after GET": {
            "data": "\r\nGET {} HTTP/1.0\r\n".format(urn)
            + "Host: {}\r\nConnection: close\r\n\r\n".format(host),
            "fragment_size": 0,
            "fragment_count": 0,
        },
        "tab sign after hostname": {
            "data": "GET {} HTTP/1.0\r\n".format(urn)
            + "Host: {}\t\r\nConnection: close\r\n\r\n".format(host),
            "fragment_size": 0,
            "fragment_count": 0,
        },
        "fragmented header": {
            "data": "GET {} HTTP/1.0\r\n".format(urn)
            + "Host: {}\r\nConnection: close\r\n\r\n".format(host),
            "fragment_size": 2,
            "fragment_count": 6,
        },
        "dot after hostname": {
            "data": "GET {} HTTP/1.0\r\n".format(urn)
            + "Host: {}.\r\nConnection: close\r\n\r\n".format(host),
            "fragment_size": 0,
            "fragment_count": 0,
        },
        " hoSt instead Host": {
            "data": "GET {} HTTP/1.0\r\n".format(urn)
            + "hoSt: {}\r\nConnection: close\r\n\r\n".format(host),
            "fragment_size": 0,
            "fragment_count": 0,
        },
        " hOSt instead Host": {
            "data": "GET {} HTTP/1.0\r\n".format(urn)
            + "hOSt: {}\r\nConnection: close\r\n\r\n".format(host),
            "fragment_size": 0,
            "fragment_count": 0,
        },
        " Hostname with uppercase": {
            "data": "GET {} HTTP/1.0\r\n".format(urn)
            + "Host: {}\r\nConnection: close\r\n\r\n".format(host.upper()),
            "fragment_size": 0,
            "fragment_count": 0,
        },
        "missing space sign after Host:": {
            "data": "GET {} HTTP/1.0\r\n".format(urn)
            + "Host:{}\r\nConnection: close\r\n\r\n".format(host),
            "fragment_size": 0,
            "fragment_count": 0,
        },
        "unix style line break in header": {
            "data": "GET {} HTTP/1.0\n".format(urn)
            + "Host: {}\nConnection: close\n\n".format(host),
            "fragment_size": 0,
            "fragment_count": 0,
        },
        "unusual order of connection and hostname": {
            "data": "GET {} HTTP/1.0\r\n".format(urn)
            + "Connection: close\r\nHost: {}\r\n\r\n".format(host),
            "fragment_size": 0,
            "fragment_count": 0,
        },
        "fragmented header, hoSt and missed space": {
            "data": "GET {} HTTP/1.0\r\n".format(urn)
            + "hoSt:{}\r\nConnection: close\r\n\r\n".format(host),
            "fragment_size": 2,
            "fragment_count": 6,
        },
    }
    return requests


def test_dpi(site, port, html_file, txt_file):
    results = []
    requests = configure_request_body(site, "/")
    for testname in sorted(requests):
        test = requests[testname]
        try:
            result = send_request(
                site,
                port,
                test.get("data"),
                html_file,
                txt_file,
                test.get("fragment_size"),
                test.get("fragment_count"),
            )
        except Exception as e:
            print("🤬 error: ", repr(e))
        else:
            if result.split("\n")[0].find("200 ") != -1:
                print("😘 open successfully")
                results.append(testname)
            else:
                print("😒 can't open")
    return list(set(results))


def main():
    html_file = "result.html"
    txt_file = "result.txt"
    site = "lenta.ru"
    port = 80

    results = test_dpi(site, port, html_file, txt_file)

    print(results)

    with open(html_file, "a") as f:
        for item in results:
            f.write("%s<br>\n" % item)

    with open(txt_file, "a") as f:
        for item in results:
            f.write("%s\n" % item)


if __name__ == "__main__":
    main()
