from functions import modinv

def add(x1,y1, x2, y2, d, n):
    numerator_x = ((x1*y2 % n) + (x2*y1 % n)) % n
    denominator_x = (1+(d*x1*x2*y1*y2)) % n
    x3 = (numerator_x * modinv(denominator_x, n)) % n

    numerator_y = ((y1*y2 % n) - (x1*x2 % n)) % n
    denominator_y = (1-(d*x1*x2*y1*y2)) % n

    y3 = (numerator_y * modinv(denominator_y, n)) % n
    return x3, y3

# values to change
d = 12           # d parameter in edwards curve
n = 17          # number of element of the field
org_x = 5       # x coordinate of P
org_y = 4       # y coordinate of P

org_x2= 13
org_y2= 12

x, y = add(org_x, org_y, org_x2, org_y2, d, n)
print(x, y)
