from functions import modinv

""" Translate a point P from Edward to 
Montgomery curve """

# values to change
x = 5      # x coordinate of P
y = 4      # y coordinate of P
p = 17     # number of elements in the group

u =( (1+y)*(modinv((1-y)%p, p)) ) % p
v = ( u*modinv(x,p) ) % p

print(f"u=(1+y)/(1-y)=(1+({y}))/(1-({y})) -> u = {u} mod {p}")
print(f"v=u/x={u}/{x} -> v = {v} mod {p}")
print(f"Point in Montgomery curve is P'=({u},{v})")
