import http.client

import requests
import socket
import ssl

from requests import ReadTimeout
from requests.exceptions import SSLError
from urllib3 import HTTPConnectionPool

html_file_with_results = "result.html"
txt_file_with_results = "result.txt"
logs_file = "result.log"

# cache_disabling_header = {'Cache-Control': 'no-cache'}

cyta_payload = "This site can’t be reached due tο compliance the Council Regulation (EU) 350/2022 and with EU and National Laws, only for as long as necessary."


def find_payload(text):
    if cyta_payload in text:
        return True
    else:
        return False


def write_to_file(filename, data):
    with open(filename, "w") as f:
        f.write("%s\n" % data)


def send_request(
        host, port,
        fragment_size=0, fragment_count=0, is_https=True):
    try:
        if is_https:
            url = f"https://{host}:{port}"
        else:
            url = f"http://{host}:{port}"
        response = requests.get(url,allow_redirects=True,timeout=3)
        response_for_df = {
            "Website": url,
            "test_name": "test_warp",
            "HTTP status code": response.status_code,
            "Success": response.status_code == 200,
            "Redirected to ISP Payload": find_payload(response.text)
        }
        # print(response.text)
        recv_decoded = response.text
        # print(recv_decoded)
        return response_for_df
    except requests.exceptions.ReadTimeout as e:
        print(f"ReadTimeout occurred: {e}")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def trucate_https(domain):
    domain = domain.replace("https://", "")
    domain = domain.replace("http://", "")
    domain = domain.replace("www.", "")
    if domain.endswith("/"):
        domain = domain[:-1]
    return domain


def get_redirection(url, timeout=5):
    print(f"Trying {url}")
    try:
        response = requests.get(f"https://{url}", allow_redirects=True,timeout=timeout)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, False, type(e).__name__

    max_redirects = 10
    num_redirects = 0
    redirect_url = f"https://{url}"
    is_https = False

    # while response.is_redirect or response.is_permanent_redirect:
    #     if num_redirects >= max_redirects:
    #         print("Reached maximum number of redirects.")
    #         break
    #
    #     redirect_url = response.headers['Location']
    #     print(f"Redirecting to: {redirect_url}")
    #
    #     try:
    #         response = requests.get(redirect_url, allow_redirects=False, timeout=timeout)
    #     except requests.exceptions.RequestException as e:
    #         print(f"An error occurred: {e}")
    #         return None, False, type(e).__name__
    #
    #     num_redirects += 1

    redirect_url = trucate_https(redirect_url)
    print("after redirections: " + redirect_url)
    return redirect_url, is_https, response.status_code


def test_http_or_https(site):
    redirected_site, is_https_required, status_code = get_redirection(site)
    if redirected_site is not None:
        return send_request(redirected_site, port=443, is_https=True)
    else:
        return {
            "Website": site,
            "test_name": "test_warp",
            "HTTP status code": status_code,
            "Success": False,
            "Redirected to ISP Payload": False
        }
