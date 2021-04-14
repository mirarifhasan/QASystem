from urllib import request as urlrequest

PROXY_ADDRESS= '220.150.77.91:6000'
url= 'http://icanhazip.com'
request = urlrequest.Request(url)
request.set_proxy(PROXY_ADDRESS, 'http')
response= urlrequest.urlopen(request)
print(response.read().decode('utf8'))
