#!/usr/bin/env python3
import requests, re

url, auth = 'url', ('', 'password')
sid, token = 1111111, 'token'

req = requests.Session()
req.cookies['token'] = token

r = req.get(url+'/', auth=auth)
ciphertext = bytes.fromhex(re.search('target_ciphertext = ([0-9a-f]+)', r.text).groups()[0])

def oracle(cipher):
    assert hasattr(cipher,'hex') and len(cipher) % 16 == 0 and len(cipher) >= 32
    r = req.post(url+'/oracle', auth=auth, data={'cipher': cipher.hex()})
    return bool(['False', 'True'].index(r.text.strip()))

def validate(plaintext):  # use this to submit your plaintext once you've decrypted it
    if type(plaintext) == bytes:
        try: plaintext = plaintext.decode()
        except UnicodeDecodeError: raise Exception('plaintext is printable ASCII; something is amiss.')
    assert type(plaintext) == str
    r = req.post(url+'/validate', auth=auth, data={'plaintext': plaintext})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

# XOR two 16-byte blocks
def xor(xs, ys):
    assert len(xs) == len(ys) == 16
    return bytes(x ^ y for x, y in zip(xs, ys))

################################################################

def split_blocks(data):
    """ Split ciphertext in blocks of 16 byte data"""
    length = len(data)
    blocks = []
    for i in range(length // 16):
        blocks.append(data[i*16:(i+1)*16])
    return blocks


def find_bytes(blocks):
    """ Retrieve 1 block plaintext """
    c_prime = bytearray([b for b in blocks[0]])

    plaintext_bytes = bytearray([0 for _ in range(16)])

    for i in range(16):
        expected_padding = bytearray([0 for _ in range(16-i)] + [(i+1) for _ in range(i)])
        c_prime = bytearray(xor(xor(expected_padding,plaintext_bytes),blocks[0]))

        for byte in [*range(blocks[0][15-i] + 1,256), *range(0,blocks[0][15-i] + 1)]:
            c_prime[15-i] = byte
            to_test = c_prime + blocks[1]
            if oracle(to_test):
                temp = byte ^ (i+1) ^ blocks[0][15-i]
                plaintext_bytes[15-i] = temp
                break
    return "".join([chr(b) for b in plaintext_bytes if b > 16])


def find_plaintext(ciphertext):
    """ Retrieve the whole plaintext """
    ciphertext = bytearray(ciphertext)
    blocks = split_blocks(ciphertext)

    plaintext = ""

    for i in range(len(blocks)-1):
        plaintext += find_bytes(blocks[i:i+2])

    return plaintext

plain = find_plaintext(ciphertext)
print("Message decrypted:")
print(plain)
validate(plain)
