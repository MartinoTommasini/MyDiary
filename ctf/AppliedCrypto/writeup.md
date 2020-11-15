# Description

put picture
and code

## Solution

The goal of the challange is to forge a signature for a message that has never been signed before. The attack is possible because the signature scheme uses only the first 5 bytes of the SHA256's output. 

The attack used is a variant of the index calculus attack.


1. Fix an upper bound y (factor base)
        - how can i choose it?
        - too large values 
        - the number of column in the matrix is number of primes in the factor base right?
The approach used is: bruteforce the messages that factors in the factor base
