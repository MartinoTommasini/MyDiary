from sympy import factorint
from sympy.ntheory.modular import crt

""" Break the DLP of h using Pohlig-Hellman
    method """

# values to change
g=11     # generator of the group
h=5705   # target of the DLP: find its exponent
p=29009   # number of elements of the group

# factor p-1
p_1 = p - 1

modulus = []
bases   = []

factors = factorint(p_1)
factors = [ x**factors[x] for x in factors ]

for factor in factors:
    print(f"Consider subgroup of order {factor}")
    # compute tables of g
    g_table = {}
    for i in range(0,factor):
        g_i = pow(g,i*(p-1)//factor,p)
        g_table[g_i] = i 

    # compute h^((p-1)/factor) modulo p
    h_factor = pow(h,(p-1)//factor,p)
    print(f"h^((p-1)/{factor})={h_factor}")

    # find match
    a = g_table[h_factor]
    bases.append(a)
    modulus.append(factor)
    print(f"g^({a}*(p-1)/{factor})={h_factor}")
    print(f"---> a={a} mod {factor}")
    print()
    print()

print("Since the modulus are pairwise coprime, we can solve \
the system of congruences using the CRT")
a,n = crt(modulus,bases)
print()
print(f"The exponent is a={a} mod {n}")
