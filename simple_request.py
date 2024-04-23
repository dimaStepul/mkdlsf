# for convenience
from requests_doh import DNSOverHTTPSSession

# By default, DoH provider will set to `cloudflare`
session = DNSOverHTTPSSession(provider='cloudflare-security')
r = session.get('https://vk.com'    )
print(r.status_code)
print(r.is_redirect)
print(r.is_permanent_redirect)
print(r.history)
print(r.content)


print(r.url)