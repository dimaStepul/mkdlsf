import ssl
ssl.HAS_SNI = False
import requests

def check_sni_blocking():
    domains = ['vk.com', 'google.com', '1xbet.com']
    blocked_domains = []

    for domain in domains:
        try:
            response = requests.get('https://' + domain)
            if response.status_code == 200:
                print("SNI is not blocked for", domain)
            else:
                print("SNI might be blocked for", domain)
                blocked_domains.append(domain)
        except Exception as e:
            print("Error occurred while accessing", domain, ":", e)
            blocked_domains.append(domain)

    if blocked_domains:
        print("Blocked domains:", blocked_domains)
    else:
        print("No domains appear to be blocked.")


if __name__ == "__main__":
    check_sni_blocking()
