#!/usr/bin/env sage 

import sys, requests, re, hashlib

from sage.all import *
from collections import OrderedDict

hashlen = 5

url, auth = 'http://131.155.21.174:8081', ('', 'ilovecrypto')
sid, token = yourSid, 'yourtoken'

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
    #print("sha")
    #print(sha(m))
    #print("hash of m")
    #print(pow(s,e,n))
    return pow(s, e, n) == sha(m)

def forgery(m, s):  # use this to submit your forgery once you've created it
    assert validate(m, s)
    r = req.post(url+'/validate_forgery', auth=auth, data={'msg': m, 'sig': str(s)})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

################################################################

def hash_and_normalize(message):
    hashed = sha(message)
    factors = OrderedDict(factor(hashed))
    # return in the form [0,0,3,2,3,0,0,2,3,1]
    return  [ factors[p] if p in factors else 0 for p in primes]


def square_multiply(x, y, N):
    exp = bin(y)
    value = x
 
    for i in range(3, len(exp)):
        value = (value * value) % N
        if(exp[i:i+1]=='1'):
            value = (value*x) % N
    return value
    




factor_base=30
num_primes = 10 # number of primes in the factor base
m_to_sign = 'twIipROLHkJWL' # message we forge the signature for. 

primes = [2,3,5,7,11,13,17,19,23,29]

# messages are linear indepenents
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

# matrix in the finite field of e elements
M = matrix(GF(e),10,10)

index=0
for message in messages:
    vect = hash_and_normalize(message)
    # insert vector in the matrix
    M[index] = vect
    index += 1

print(M)

# express the hash of the message we want to forge the signature for as a vector
vect = hash_and_normalize(m_to_sign) 
w = vector(GF(e),vect)

# we express w as a linear combination of the other vectors
w_comb = M.solve_right(w) 


# let the oracle sign the messages (expept for our target message)
i=0
tot=1
for m in messages:
    #temp = Mod(sign(m)**w_comb[i],n)
    temp = square_multiply(sign(m),int(w_comb[i]),n)
    tot = Mod(tot * temp,n)
    i += 1


#for p in primes:
#    tot = Mod(tot*p,n)


print("message:")
print(m_to_sign)
print("forgery:")
print(tot)

#forgery(m_to_sign,tot)
