from math import floor, sqrt
from functions import modinv

""" Use Baby step giant step to break the DLP
    in groups of p elements """

# values to change
p = 4327  # number of elements in the field
l = 103      # group order of the field
g = 1914   # generator of the field
h = 2045  # target of the bsgs. Find its exponent

# g and h are both in modulo p
print(f"Break the DLP of h={h}")
print(f"p={p}, l={l}, g={g}")
print()

# compute m
m=floor(sqrt(l))
print(f"Compute m=floor(sqrt(l))={m}")

print("Baby steps")
# baby steps
baby_table={}
for i in range(0,m):
    x = pow(g,i,p)
    baby_table[x] = i
    print(f"g{i}={x}")
print()

# compute g inverse to speed up
# ginv = pow(g,-m,p)  can't compute a negative exponent
ginv = pow(modinv(g,p),m,p)
print(f"Compute the inverse ginv=g^(-{m})={ginv}")
print()

print("Giant steps")
# giant steps
for j in range(0,m):
    x = (h*pow(ginv,j,p)) % p
    print(f"h*ginv^{j}={x}")
    if x in baby_table:
        a = baby_table[x] + j*m
        print()
        print(f"Match found: i={baby_table[x]}   j={j}")
        print(f"a = i + m*j = {baby_table[x]} + {m}*{j}")
        print(f"a={a}")
        exit(0)

