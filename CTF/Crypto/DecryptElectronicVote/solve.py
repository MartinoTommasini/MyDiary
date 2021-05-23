#! /usr/bin/python3

import sys, requests, re, random


url, auth = 'url', ('', 'pass')
sid, token = 111111, 'token'

req = requests.Session()
req.cookies['token'] = token

def submit(v):
    r = req.post(url+'/validate', auth=auth, data={'sol': v})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

def square_multiply(x, y, N):
    exp = bin(y)
    value = x
 
    for i in range(3, len(exp)):
        value = (value * value) % N
        if(exp[i:i+1]=='1'):
            value = (value*x) % N
    return value

def is_exp_even(gx):
    """ Return true if exponent is even """
    return square_multiply(gx,q,p) == 1


p = 57774818814943754116448518184326452823721631810927458932866919137141138307753611224327604381007167692829083988610548043160788041791018317339818651327580610411738986484381094405741763088828758443400838032158591609385757184412373898110764353557827938954768478153759084755885826758206520943108899670595846176019
q = (p-1)//2
h = 8378442675337480300699837294881012494019618445640276803837055888811813204500740784741863347994273874706730460773882011722595536297336226155722053240423395303849323789553857510063958083304606564167426282395216721250644006819970724538088197414939384647516005726480256427847280118020312237344472234563203247636

if is_exp_even(h):
    print("g^x is a square -> x is even")
else:
    print("g^x not a square -> x is odd")

# from now on I consider that g^x is even

votes = []
with open("encrypted_votes.txt") as f:
    for line in f.readlines():
        g_r, g_r_votes = [ int(x) for x in line.split(",") ]
        if is_exp_even(g_r_votes):
            votes.append("1")
        else:
            votes.append("2")


# convert list of votes to string of votes with delimiter ","
votes_str = ",".join(map(str,votes))
print(votes_str)
submit(votes_str)
            




