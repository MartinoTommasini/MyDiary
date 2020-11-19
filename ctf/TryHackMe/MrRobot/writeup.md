# Mr Robot
Find the 3 hidden flags

## Solution

ip=10.10.231.112
First, we scan the box using nmap

```
> nmap -sC -sV 10.10.231.112 -oN nmap-initial

Starting Nmap 7.91 ( https://nmap.org ) at 2020-11-16 23:57 CET
Nmap scan report for 10.10.231.112
Host is up (0.046s latency).
Not shown: 997 filtered ports
PORT    STATE  SERVICE  VERSION
22/tcp  closed ssh
80/tcp  open   http     Apache httpd
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
443/tcp open   ssl/http Apache httpd
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
| ssl-cert: Subject: commonName=www.example.com
| Not valid before: 2015-09-16T10:45:03
|_Not valid after:  2025-09-13T10:45:03
```

We know that port 80 is open. Let's visit it.  
Entering http://10.10.231.112 we have a terminal. 

As a first step we study the different commands the terminal provides. 
Using the _join_ command we then get asked to provide an email. We can set up a temporary mail and give it. Seems a void feature, no messages are sent to the provided email.  
We start looking in other directions.


The name of the box is Mr Robot. Visiting the robot.txt file we get 
```
User-agent: *
fsocity.dic
key-1-of-3.txt
```
Now with http://10.10.231.112/key-1-of-3.txt we get the first flag
```
073403c8a58a1f80d943455fb30724b9
```

Visiting https.//10.10.231.112/fsocity.dic we can download a txt file. Presumibely, it's a dictionary file we can use to bruteforce some logins

Running gobuster to scan hidden directories
```
gobuster dir -u http://10.10.231.112 -t 64 -w /usr/share/wordlists/rockyou.txt
```

In http://10.10.231.112/wp-login.php we have a login form. We try to login as admin, bruteforcing the password using using Hydra and the fsocity.dic as wordlist file.

