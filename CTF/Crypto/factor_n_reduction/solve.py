#!/usr/bin/env python3
import sys, requests, re, random

from math import gcd

url, auth = 'url', ('', 'pass')
sid, token = 1111111, 'token'

req = requests.Session()
req.cookies['token'] = token

r = req.get(url+'/', auth=auth)
n = int(re.findall('n = ([0-9]+)', r.text)[0])

def sqrt(x):
    r = req.post(url+'/sqrt', auth=auth, data={'value': x})
    if r.text.strip() == 'None': return None  # not a square
    return int(r.text)

def factorization(p, q):  # use this to submit your factorization
    assert type(p) == type(q) == int
    r = req.post(url+'/validate_factorization', auth=auth, data={'p': '{:d}'.format(p), 'q': '{:d}'.format(q)})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

################################################################

print('n: {}'.format(n))

# use the square root oracle to compute the factorization of n

while True:
    # pick a number x 
    x = random.randrange(n)
    print("x: {}".format(x))

    # compute the x^2
    x_2 = pow(x,2,n)

    # give x^2 to the oracle and get the result y
    y=sqrt(x_2)
    print("y: {}".format(y))

    if not y or x==y or x==-y:
        continue

    # if y != x then we have that gcd(x-y,n) is a factor
    p = gcd(x-y,n)
    q = n // p
    print("Found factors")
    print("p={}".format(p))
    print("q={}".format(q))
    factorization(p,q)
    break
    

