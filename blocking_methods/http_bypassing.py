import requests
import socket
import ssl

html_file_with_results = "result.html"
txt_file_with_results = "result.txt"
logs_file = "result.log"


def write_to_file(filename, data):
    with open(filename, "w") as f:
        f.write("%s\n" % data)


def _decode_bytes(input_bytes):
    return input_bytes.decode(errors="replace")


def send_request(
        host, port, data, html_file, txt_file,
        fragment_size=0, fragment_count=0, is_https=True):
    sock = socket.create_connection((host, port), 10)
    if is_https:
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=host)

    if fragment_count:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

    try:
        for fragment in range(fragment_count):
            write_to_file(html_file, "fragment" + str(fragment))
            write_to_file(txt_file, "fragment" + str(fragment))

            sock.sendall(data[:fragment_size].encode())
            data = data[fragment_size:]

            write_to_file(html_file, str(data))
            write_to_file(txt_file, str(data))

        sock.sendall(data.encode())
        recvdata = sock.recv(8192)
        recv = recvdata
        recv_decoded = recv.decode()
        print(recv_decoded)
        write_to_file(logs_file, recv_decoded)
        write_to_file(html_file, recv_decoded)
        write_to_file(txt_file, recv_decoded)
        while recvdata:
            recvdata = sock.recv(8192)
            recv += recvdata
    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except  Exception:
            print("Exception occurred")
        sock.close()
    return _decode_bytes(recv)


def configure_request_body(host, urn="/"):
    requests_body = {
        "normal one ": {
            "data": "GET {} HTTP/1.1\r\n".format(urn)
                    + "Host: {}\r\nConnection: close\r\n\r\n".format(host),
            "fragment_size": 0,
            "fragment_count": 0,
        },
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
    return requests_body


def test_dpi(site, port, html_file=html_file_with_results,
             txt_file=txt_file_with_results, is_https=False):
    results = []
    configured_requests = configure_request_body(site, "/")
    for test_name in sorted(configured_requests):
        test = configured_requests[test_name]
        try:
            result = send_request(
                site,
                port,
                test.get("data"),
                html_file,
                txt_file,
                test.get("fragment_size"),
                test.get("fragment_count"),
                is_https,
            )

            # for i in range(10):
            #     print(result.split("\n")[i])



        except Exception as e:
            print("🤬 error: ", repr(e))
        else:
            if result.split("\n")[0].find("200 ") != -1:
                print("😘 open successfully")
                results.append(test_name)
            else:
                print("😒 can't open")
    return list(set(results))


def trucate_https(domain):
    domain = domain.replace("https://", "")
    domain = domain.replace("http://", "")
    domain = domain.replace("www.", "")
    if domain.endswith("/"):
        domain = domain[:-1]
    return domain


def get_redirection(url):
    response = requests.get(f"http://{url}", allow_redirects=False)
    max_redirects = 10
    num_redirects = 0
    redirect_url = f"http://{url}"
    is_https = False
    while response.is_redirect or response.is_permanent_redirect:
        if num_redirects >= max_redirects:
            print("Reached maximum number of redirects.")
            break

        redirect_url = response.headers['Location']
        if redirect_url.find("https") != -1:
            is_https = True
        print(f"Redirecting to: {redirect_url}")
        response = requests.get(redirect_url, allow_redirects=False)
        num_redirects += 1
    redirect_url = trucate_https(redirect_url)
    print(redirect_url)
    return redirect_url, is_https


def test_http_or_https(site):
    site, is_https_required = get_redirection(site)
    if is_https_required:
        port = 443
    else:
        port = 80
    test_dpi(site, port=port, is_https=is_https_required)


def main():
    site = "ria.ru"
    test_http_or_https(site)


if __name__ == "__main__":
    main()
