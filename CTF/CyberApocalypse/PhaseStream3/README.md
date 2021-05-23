
# Nonce reuse
The nonce used in the encryption of the flag is the same used in the encryption of the *test* message.  

By looking at the working principle of AES in counter mode, we see that we can compute the *flag* plaintext without knowing the nonce as: (for 1 byte)

```
byte1_flag = byte1_chiper_test XOR byte1_chiper_flag XOR byte1_plain_test
```

We get the entire flag by repeating it for the other bytes.  

AES in CTR mode returns a ciphertext which is the same size of the plaintext.  
Thus, the number of bytes to recover is given by the number of bytes in the *flag* ciphertext.

```python
c_test = '464851522838603926f4422a4ca6d81b02f351b454e6f968a324fcc77da30cf979eec57c8675de3bb92f6c21730607066226780a8d4539fcf67f9f5589d150a6c7867140b5a63de2971dc209f480c270882194f288167ed910b64cf627ea6392456fa1b648afd0b239b59652baedc595d4f87634cf7ec4262f8c9581d7f56dc6f836cfe696518ce434ef4616431d4d1b361c'

c_flag = '4b6f25623a2d3b3833a8405557e7e83257d360a054c2ea'

c_test = bytes.fromhex(c_test)
c_flag = bytes.fromhex(c_flag)

p_test = b"No right of private conversation was enumerated in the Constitution. I don't suppose it occurred to anyone at the time that it could be prevented."


flag = ''
for i in range(len(c_flag)):
    plain_byte = p_test[i] ^ c_test[i] ^ c_flag[i]
    flag += chr(plain_byte)

print(flag)

```

