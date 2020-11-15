#!/usr/bin/env sage

from sage.all import *

bound = 2**30

P = Primes()

i=0
for prime in P:
    print(prime)
    i += 1
    if i >= bound:
        exit(1)

