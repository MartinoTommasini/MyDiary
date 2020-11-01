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
d = 234           # d parameter in edwards curve
n = 239          # number of element of the field
org_x = 110       # x coordinate of P
org_y = 211       # y coordinate of P

print(org_x, org_y)
x, y = add(org_x, org_y, org_x, org_y, d, n)
print(x, y)
i = 2
while not(x == 0 and y == 1):
    x, y = add(org_x, org_y, x, y, d, n)
    print(x, y)
    i += 1
print("Order: %i" % i)
