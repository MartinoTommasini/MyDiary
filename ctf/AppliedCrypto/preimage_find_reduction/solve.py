#!/usr/bin/env python3
import sys, requests, re, random, os

url, auth = 'url', ('', 'pass')
sid, token = 1111111, 'token'

req = requests.Session()
req.cookies['token'] = token

r = req.get(url+'/', auth=auth)
target = bytes.fromhex(re.search('target_hash = ([0-9a-f]+)', r.text).groups()[0])

def hash(x):
    r = req.post(url+'/hash', auth=auth, data={'data': x.hex()})
    return bytes.fromhex(r.text)

def multi_unhash(xs):
    r = req.post(url+'/multi_unhash', auth=auth, data={'hashes': [x.hex() for x in xs]})
    r = r.text.strip().split()
    if r[1] == 'None': return int(r[0]), None  # bad query
    return int(r[0]), bytes.fromhex(r[1])

def preimage(x):  # use this to submit your preimage
    r = req.post(url+'/validate_preimage', auth=auth, data={'data': x.hex()})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

################################################################

print('target hash value: {}'.format(target.hex()))

while True:
    hashes = []

    # generate 24 hashes
    for _ in range(24):
        x = os.urandom(random.randrange(5,20))
        hashes.append(hash(x))

    # insert the target hash, hoping that the oracle decrypts it
    # I noticed that the oracle never replies with the decryption of the
    # hash at index 0 or 24. Therefore I insert the hash in the 23rd position
    hashes.insert(23,target)


    # query the multi target oracle
    pre_image = multi_unhash(hashes)
    print("Oracle is decrypting")
    print(pre_image)
    print("")

    if pre_image[0] == 23:
        print("Preimage  of target found".format(target))
        preimage(pre_image[1])
        print(pre_image[1].hex())
        break

