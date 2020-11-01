from sympy.ntheory.modular import crt

""" Use Chinese Remainder Theorem to 
efficiently decrypt the message using p and q """

print("Use Chinese Remainder Theorem to efficiently decrypt the message using p and q")

# values to change
c = 153497       # chipertext to decrypt
d = 149453       # private key of receiver
p = 673       # factor of n
q = 557       # factor of n

print("Reduce the exponent modulo phi(exponent) where phi is the\
Euler's totient function")
print("phi(exponent) = exponent - 1 if exponent is prime")

dp = d % (p-1)
dq = d % (q-1)
print(f"dp = d % (p-1) = {dp}")
print(f"dq = d % (q-1) = {dq}")
print()

print("Now we reduce the base")
cp = c % p
cq = c % q
print(f"cp = c % p = {cp}")
print(f"cq = c % q = {cq}")

print("Therefore we have:")
print("m = {cp}^{dp} mod {p}")
print("m = {cq}^{dq} mod {q}")
print()
print("Since p and q are pairwise coprime, we can compute the message using the CRT")

mp = pow(cp,dp,p)
mq = pow(cq,dq,q)

m,n = crt([p,q],[mp,mq])

print(f"The message is {m}")
