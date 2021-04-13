# My solution

If N is small, then we can simply factor it.  

We factor N using PariGp. The factors are:  
`p=2159947535959146091116171018558446546179`
`q=658558036833541874645521278345168572231473`

We can now compute the private key d as:
d=e^{-1} mod((p-1)(q-1)
d=975120122884150896343356420256053234758228648361853546720066993334766006694511009

We can compute the message m as:
m=c^d modN
m=13016382529449106065927291425342535437996222135352905256639555294957886055592061

We can convert the message from decimal to ascii with:
```
bytearray.fromhex(hex(m)[2:]).decode()
```

We get our flag
flag: picoCTF{sma11_N_n0_g0od_00264570}
