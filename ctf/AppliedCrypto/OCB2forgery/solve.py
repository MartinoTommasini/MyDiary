#!/usr/bin/env python3

import requests
import random

url, auth = 'url', ('', 'password')
sid, token = 1111111, 'your token'

req = requests.Session()
req.cookies['token'] = token

def encrypt(nonce, plain):
    assert hasattr(nonce,'hex') and hasattr(plain,'hex') and len(nonce) == 16
    r = req.post(url+'/encrypt', auth=auth, data={'nonce': nonce.hex(), 'plain': plain.hex()})
    return tuple(map(bytes.fromhex, r.text.strip().split()))

def decrypt(nonce, cipher, tag):
    assert hasattr(nonce,'hex') and hasattr(cipher,'hex') and hasattr(tag,'hex') and len(nonce) == len(tag) == 16
    r = req.post(url+'/decrypt', auth=auth, data={'nonce': nonce.hex(), 'cipher': cipher.hex(), 'tag': tag.hex()})
    if 'INVALID' in r.text: return
    return bytes.fromhex(r.text.strip())

def forgery(nonce, cipher, tag):  # use this to submit your forgery once you've created it
    assert type(nonce) == type(cipher) == type(tag) == bytes
    assert len(cipher) >= 33 and len(nonce) == len(tag) == 16
    r = req.post(url+'/validate_forgery', auth=auth, data={'nonce': nonce.hex(), 'cipher': cipher.hex(), 'tag': tag.hex()})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

# XOR two 16-byte blocks
def xor(xs, ys):
    assert len(xs) == len(ys) == 16
    return bytes(x ^ y for x, y in zip(xs, ys))

################################################################


alphabet = "abcdefghijklmnopqrstuvwyz"

# using 4 message block of 16 byte each. Message has 16*4=62 bytes

# in 16 bytes ( 128 bits) the len(O^n) is 0{120}10{7} = 0x80
# build the 4-block message such that M[m-1] = len(O^n)
# crafting the message
m_hex = '10'*32+'00'*15+'80'+'10'*16
m = bytes.fromhex(m_hex)


# take an arbitrary nonce
nonce = bytes(''.join(random.choice(alphabet) for _ in range(16)), 'utf-8')
print('nonce: {} ({})'.format(nonce.hex(), repr(nonce)))

# let the oracle encrypt
cipher, tag = encrypt(nonce, m)

# craft the forged ciphertext
forged_c = []

forged_c[:16*2] = cipher[:16*2]
checksum = xor(m[:16], m[16:32])
temp = xor(cipher[32:48], m[32:48])
forged_c[32:48] = xor(temp, checksum)
forged_c_byte = bytes(forged_c)
print('forged ciphertext: {} ({})'.format(forged_c_byte.hex(), repr(forged_c_byte)))

# craft the forged valid tag
forged_tag = xor(m[48:], cipher[48:])
print('forged_tag: {} ({})'.format(forged_tag.hex(), repr(forged_tag)))

# let the oracle decrypt
plain2 = decrypt(nonce, forged_c_byte, forged_tag)

if plain2:
    print('decrypted (correct): {} ({})'.format(plain2.hex(), repr(plain2)))
    print("Forgery successful. Sending forgery.")
    #forgery(nonce,forged_c_byte,forged_tag)
else:
    print("Forgery not successful")
