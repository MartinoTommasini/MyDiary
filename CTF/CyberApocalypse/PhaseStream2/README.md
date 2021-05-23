
# Solution

Same as PhaseStream1 but we know the key is 1 byte this time.  
For each ciphertext, we try the likely bytes.  
For the correct key byte, the decryption will be our flag.

```python
import string

alphabet = list(string.ascii_letters)

i=0
with open("output.txt","r") as f:
    for line in f.readlines():
        ciphertext = line.strip()
        for key_guess in alphabet:
            plain = "".join(chr(ord(x)^ord(y)) for x, y in zip(bytes.fromhex(ciphertext).decode("latin-1"), key_guess*100))
            if plain.startswith("CHTB{"):
                print("Flag found: ")
                print(plain)
                exit(1)
```
Not very efficient, but does its job.  


Flag: `CHTB{n33dl3_1n_4_h4yst4ck}`