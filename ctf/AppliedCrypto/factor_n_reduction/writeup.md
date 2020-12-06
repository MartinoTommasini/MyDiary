# Description

Compute the factorization of a RSA modulo using an oracle that computes a square root modulo an RSA number n

## Solution

1. Pick a random number x  in the finite field.
2. Compute the x^2
3. Give the x^2 to the oracle and store the result in y
4. if x==y or x==-y, we are unlucky and we return to step 2. Else we were lucky!
5. p = gcd(x-y,n) is one factor
6. n / p is the other factor
