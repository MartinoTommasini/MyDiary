#!/usr/bin/env sage
import sys, requests, re, hashlib
from sage.all import factor
import random, string

hashlen = 5

url, auth = 'url', ('', 'passwor')
sid, token = 1111111, 'token'

sha = lambda m: int(hashlib.sha256((str(sid) + m).encode()).hexdigest()[:2*hashlen],16)

req = requests.Session()
req.cookies['token'] = token

r = req.get(url+'/', auth=auth)
n = int(re.search('n = ([0-9]+)', r.text).groups()[0])
e = int(re.search('e = ([0-9]+)', r.text).groups()[0])


def sign(m):
    r = req.post(url+'/sign', auth=auth, data={'msg': m})
    return int(r.text)

def validate(m, s):
    return pow(s, e, n) == sha(m)

def forgery(m, s):  # use this to submit your forgery once you've created it
    assert validate(m, s)
    r = req.post(url+'/validate_forgery', auth=auth, data={'msg': m, 'sig': str(s)})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

################################################################



print('public key: {}'.format((n,e)))

# Find messages that factor in the factor base 
factor_base= 14
alphabet ="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&"

cont=0
while True:
    message =  ''.join(random.choice(alphabet) for _ in range(13) )
    hashed=sha(message)
    if factor(hashed)[-1][0] <= factor_base:
        print(message)
        cont += 1

# run the script till you need

