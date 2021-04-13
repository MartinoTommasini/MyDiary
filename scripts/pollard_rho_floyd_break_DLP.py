def pollard_helper(x,b,c,p,g,h):
    if x % 3 == 0:
        x = (x*g) % p
        b += 1
        c = c
    elif x % 3 == 1:
        x = (x*h) % p
        b = b
        c += 1
    elif x % 3 == 2:
        x = pow(x,2,p)
        b = 2*b
        c = 2*c
    else:
        print("Errore in pollard helper. x: "+str(x))
    return x,b,c
       



# Variables
h=33176
g=9528
p=35533
b0=1
c0=0
x0=16777

# initialization slow walk
xs=x0
bs=b0
cs=c0

# initialization fast walk
xf=x0
bf=b0
cf=c0

count=0
while True:
    count += 1
    xs,bs,cs = pollard_helper(xs,bs,cs,p,g,h)
    xf,bf,cf = pollard_helper(*pollard_helper(xf,bf,cf,p,g,h),p,g,h)
    print("XS: {}, bs: {}, cs: {} -- XF: {}, bf: {}, cf: {}".format(xs,bs,cs,xf,bf,cf))
    if (xs==xf):
        print("Trovato. Count: "+str(count))
        print("bs: {}, bf: {}, cs: {}, cf: {}".format(bs,bf,cs,cf))
        exit(0)
