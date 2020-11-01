from math import gcd

""" Factor the integer n using Pollard rho method
    with Floyd's cycle """

def pollard_helper(x,n):
    temp = pow(x,2,n)
    result = (temp + t ) % n 
    print(f"Mod({x}^2+{t},{n})=Mod({result},{n}")
    return (temp + t) % n 



# Values to change
n=120781  # number to factor
x0=5   # starting point of the walk
t=1    # also the iteration function could be changed

print(f"Trying to factor n={n}. The walk starts at x0={x0}")
print()

count=0
while True:
    if count == 0:
        # Initialization: step 0
        xs=x0
        xf=x0
    else:
        # compute slow walk and fast walk
        xs = pollard_helper(xs,n)
        xf = pollard_helper(pollard_helper(xf,n),n)
    d = gcd(xf-xs,n)
    print(f"{count}:")
    print(f"xs={xs}")
    print(f"xf={xf}")
    print(f"gcd({xf}-{xs},{n})={d}")
    print()
    # exclude trivial factors
    if d != 1 and d != n:
        print("Factor found at step {}.".format(count))
        print("p={}".format(d))
        q = int(n/d)
        print(f"n={d}*{q}")
        exit(0)
    count += 1
