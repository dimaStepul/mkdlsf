import requests

def check_doh_blocking():
    doh_servers = [
        {'name': 'Cloudflare', 'url': 'https://cloudflare-dns.com/dns-query'},
        {'name': 'Google', 'url': 'https://dns.google'}
    ]

    for server in doh_servers:
        try:
            response = requests.get(server['url'], params={'name': 'vk.com'}, verify=False)
            if response.status_code == 200:
                print(f"No DoH blocking detected for {server['name']} DoH server")
            else:
                print(f"DoH blocking detected for {server['name']} DoH server")
        except Exception as e:
            print(f"Error occurred while testing {server['name']} DoH server: {e}")

if __name__ == "__main__":
    check_doh_blocking()
