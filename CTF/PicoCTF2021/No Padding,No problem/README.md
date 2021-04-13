# My  solution

No padding is used. We can attack the textbook RSA having a decryption oracle.  


```python
from pwn import *

r = remote("mercury.picoctf.net",2671)

# get n,e and c
r.recvuntil("n: ")
n = int(r.recvline().strip().decode())
r.recvuntil("e: ")
e = int(r.recvline().strip().decode())
r.recvuntil("ciphertext: ")
c = int(r.recvline().strip().decode())

print("n: ",n)
print("e: ",e)
print("c: ", c)


# generate new ciphertext
s = 2
c_forged = ( c * (s**e) ) % n

# send new ciphertext to the oracle and get response
r.recvuntil("Give me ciphertext to decrypt: ")
r.sendline(str(c_forged))

# receive decrypted message
r.recvuntil("Here you go: ")
m_forged = int(r.recvline().strip().decode())

# extract original message
s_inv = pow(s,-1,n)
m = (m_forged * s_inv) % n

# print the flag
print(bytearray.fromhex(hex(m)[2:]).decode())

r.close()
```

Flag: picoCTF{m4yb3_Th0se_m3s54g3s_4r3_difurrent_5814368}

1. First we generate the new chipertext where 's' is a value of our choice ('s' and 'n' needs to be coprime)
2. We let the oracle decrypt our chipertext
3. We can extract the secret message of the original plaintext by dividing m_forged by the moltiplicative inverse of 's' in modulo n
