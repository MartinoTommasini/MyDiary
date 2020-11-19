#! /usr/bin/env sage

import sys, requests, re, hashlib
from sage.all import *
from collections import OrderedDict

hashlen = 5

url, auth = 'http://131.155.21.174:8081', ('', 'ilovecrypto')
sid, token = 1608584, '9c593b9cff2bb86750728edca1d4e203b20ee451'

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

# find linear independent vectors

factor_base=30
num_primes = 10 # number of primes in the factor base

primes = [2,3,5,7,11,13,17,19,23,29]

messages = [ 
        'wolOymtxcWggn',
        'ZxwlfbFIXneow',
        'zzlLWRpoWyWzn',
        'ZtKCYOROzJjrN',
        'iAQuGaIolTihB',
        'CPJaXVIYAQaqb',
        'aDgfOqOsSKHmG',
        'SlUgldVmvDwDm',
        'TgxMATysVJSMn',
        'NUtIMkOtgKnLs',
        ]
# to sign twIipROLHkJWL

# set the matrix with 0 values
M = matrix(GF(e),10,10)

index=0
for message in messages:
    hashed = sha(message)
    factors = OrderedDict(factor(hashed))

    vector = []
    for p in primes:
        if p in factors:
            vector.append(factors[p])
        else:
            vector.append(0)
    M[index] = vector
    index += 1

print(M)
print("-"*10)
print(M.echelon_form())
