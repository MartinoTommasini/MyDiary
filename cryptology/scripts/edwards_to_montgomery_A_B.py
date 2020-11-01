from functions import modinv
""" Find A and B coefficient to transform an
    Edward in Montgomery curve """ 

# values to change
a=1   
d=12
p=17   # elements of the field

den = modinv((a-d) % p, p)

A = ( 2*(a+d)* den ) % p
B = ( 4*den ) % p
print(f"A=2*(a+d)/(a-d)=2*({a}+({d}))/({a}-({d})) -> A = {A} mod {p}")
print(f"B=4/(a-d)=4/({a}-({d})) -> B = {B} mod {p}")
