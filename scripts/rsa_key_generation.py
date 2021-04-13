from math import gcd
from functions import modinv,egcd

""" Given p and q, generate:
    publik key (n,e)
    private key (n,d) """

# values to change
p=457
q=383
e=5
print(e)

n=p*q
print(f"n=p*q={n}")

phi=(p-1)*(q-1)
print(f"phi=(p-1)*(q-1)={phi}")

if gcd(e,phi) != 1:
    print("e and phi are not coprime. Can't generate d")
    exit(1)

d=egcd(e,phi)[1]
print("Using bezout(e,phi)")
print(f"d={d}")

# Bring d positive. d = d + phi in modulo phi
if d < 0:
    print("Transform in d positive")
    d = d + phi
    print(f"d = d + phi = {d}")

print(f"Public key:  ({n},{e})")
print(f"Private key: ({n},{d})")
