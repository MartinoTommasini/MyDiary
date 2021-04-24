# Solution

We Xor the ciphertext with the flag format.  
In this way we get the alien's key.

```
>>> "".join(chr(ord(x)^ord(y)) for x, y in zip(bytes.fromhex("2e313f2702184c5a0b1e321205550e03261b094d5c171f56011904").decode("latin-1"), "CHTB{"*100))
'mykey[\x04\x0eIeqZQ\x17u@nOK6\x1f_K\x14zZL'
```

*mykey* is the key used for the XOR.  
We can now get the whole message

```
"".join(chr(ord(x)^ord(y)) for x, y in zip(bytes.fromhex("2e313f2702184c5a0b1e321205550e03261b094d5c171f56011904").decode("latin-1"), "mykey"*100))
'CHTB{u51ng_kn0wn_pl41nt3xt}'
```
