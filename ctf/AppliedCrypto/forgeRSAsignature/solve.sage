#!/usr/bin/env sage 

import sys, requests, re, hashlib

from sage.all import factor,Mod
from collections import OrderedDict

import sympy

hashlen = 5

url, auth = 'http://131.155.21.174:8081', ('', 'ilovecrypto')
sid, token = 1608584, '40e9b9c54390bacdf9e6664aeb5ae08d89969087'

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
    #r = req.post(url+'/validate_forgery', auth=auth, data={'msg': m, 'sig': str(s)})
    #print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

################################################################

def hash_and_normalize(message):
    """ return a vector of exponents in the factor base 
        e.g.  25=5^2. 
        returns: [0,0,2,0,0,0] """

    hashed = sha(message)
    factors = OrderedDict(factor(hashed))
    return  [ factors[p] if p in factors else 0 for p in primes]


m_to_sign =  'UN2cbHO3Iy' # message we forge the signature for. 

primes = [2,3,5,7,11,13]

# messages with linear independent hash over the factor base
messages = [ 
            'tsCbMD4ZZz',
            'SOZ5u6GLeJ',
            'kX375DPEFA',
            'o7NaaXi0G3',
            'kpv1CmXUMr',
            'Ao9n7KR!DP',
         ]

M = matrix(6,6)

index=0
for message in messages:
    # insert vector in the matrix
    vect = hash_and_normalize(message)
    M[index] = vect
    index += 1

print("Message we want to forge the signature for")
print(m_to_sign)
print("")
print("Matrix of hash exponents in the factor base")
print(M)
print("")

# express the hash of the message we want to forge the signature for as a vector
vect = hash_and_normalize(m_to_sign) 
w = vector(vect)

# express w as a linear combination of the other vectors.
# take the int of the power because the result of all the expression
# would be modulo e otherwise. 
betas = int(pow(M.det(),-1,e)) * M.transpose().adjoint() * w

# espress Vj as a linear combination of the other vectors. 
# Vj mod e returns the vector vect
Vj = M.transpose() * betas

# gammas: number of times I have to subtract e to Vj in order to have w
gammas = [ int(x / e) for x in Vj]
# check
assert(vector(Vj - e*vector(gammas)) == w )

# let the oracle sign the messages (expept for our target message)
i=0
tot=1
for m in messages:
    print("Asking signature for "+m)
    temp = pow(sign(m),betas[i],n)
    tot = Mod(tot * temp,n)
    i += 1

i=0
for p in primes:
    temp = pow(p,-gammas[i],n)
    tot = Mod(tot*temp,n)
    i += 1

print("")
print("forgery:")
print(tot)

forgery(m_to_sign,tot)
