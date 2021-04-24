

# Nonce reuse without knowledge of plaintexts
Same nonce reuse we had in PhaseStream3.  

However this time we don't have the plaintext of the *test* message.  


Given that nonce is the same, then for AES in CTR mode we have that:
```
chiper_test XOR chiper_flag = plain_test XOR plain_flag
```

How can we proceed?


## Solution
We know the flag starts with `CHTB{`. We can retrieve the first 6 bytes of the *test* plaintext as done in PhaseStream3. And we get: `I alo`.

We can try to guess how `I alo` may continue. Could it be `I alone `?  
Let's consider `I alone` as our guess.  
Again as in PhaseStream3 we can retrieve 7 bytes of the flag: `CHTB{str`.  

While it would be very difficult to find our flag just by guessing what the plaintext could be, statistical or frequency analysis tools may certainly automate the task for us.  
Luckily, we can solve the challenge in a simpler way.

The *test* plaintext used in PhaseStream3 was a famous Whitfield Diffie's quote. Therefore, it may be possible that another very famous quote is again used in this challenge.


With an easy google search (`"I alone" quote`), we find a quote of Mother Teresa, Thanks God!:
```
I alone cannot change the world, but I can cast a stone across the water to create many ripples
```

It is the actual plaintext used for the *test* message.  
We can get the flag with the same script of PhaseStream3.

```python
c_test = '2d0fb3a56aa66e1e44cffc97f3a2e030feab144124e73c76d5d22f6ce01c46e73a50b0edc1a2bd243f9578b745438b00720870e3118194cbb438149e3cc9c0844d640ecdb1e71754c24bf43bf3fd0f9719f74c7179b6816e687fa576abad1955'

c_flag = '2767868b7ebb7f4c42cfffa6ffbfb03bf3b8097936ae3c76ef803d76e11546947157bcea9599f826338807b55655a05666446df20c8e9387b004129e10d18e9f526f71cabcf21b48965ae36fcfee1e820cf1076f65'

c_test = bytes.fromhex(c_test)
c_flag = bytes.fromhex(c_flag)

p_test = b"I alone cannot change the world, but I can cast a stone across the water to create many ripples"


flag = ''
for i in range(len(c_flag)):
    plain_byte = p_test[i] ^ c_test[i] ^ c_flag[i]
    flag += chr(plain_byte)

print(flag)

```

Flag: `CHTB{stream_ciphers_with_reused_keystreams_are_vulnerable_to_known_plaintext_attacks}`


