import niquests
s = niquests.Session(resolver="dot+google://", multiplexed=True)
r = s.get('https://vk.com',allow_redirects=True)
print(r.status_code)
print(r.is_redirect)
print(r.conn_info)
print(r.http_version)
print(r.content)

import requests
request = requests.get('https://vk.com',allow_redirects=True)
print(request.status_code)
print(request.is_redirect)
print(request.content)