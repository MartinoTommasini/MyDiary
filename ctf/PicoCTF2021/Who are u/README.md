# My Solution


We can change the user agent to picobrowser:
By changing the user agent to picobwrowser we get a different error message 

I don&#39;t trust users visiting from another site.

Then we use the Referer option so that the server see that the request was doneby the site itself
```
Referer: https://mercury.picoctf.net:52362
```
and we get `Sorry, this site only worked in 2018`

We can bypass this by adding the date header
```
Date: Wed, 21 Oct 2018 07:28:00 GMT
```
and we get `I don&#39;t trust users who can be tracked`

We bypass it by adding the DNT header (Do not track)
```
DNT: 1
```
and we get `This website is only for people from Sweden`

We may use a vpn located in Sweden (maybe) or we can simply take a swedish ip and add the header:
```
X-Forwarded-For: 11.11.111.111  (this is a fake ip. Make sure the ip originates from Sweden.)
```

The flag: picoCTF{http_h34d3rs_v3ry_c0Ol_much_w0w_0c0db339}u


Final request:
```
GET / HTTP/1.1
Host: mercury.picoctf.net:52362
User-Agent: picobrowser
Referer: https://mercury.picoctf.net:52362
Date: Wed, 21 Oct 2018 07:28:00 GMT
DNT: 1
Accept-Language: sv-SWE
Content-Language: sv-SWE
Content-Length: 2
```
