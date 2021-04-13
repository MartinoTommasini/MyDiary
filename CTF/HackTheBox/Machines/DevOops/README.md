# Solution

Start with a nmap enumeration

```
nmap -sV -sC -oN nmap-initial 10.10.10.91
```

Ubuntu 16.04

We run gobuster
```
gobuster dir -u http://10.10.10.91:5000/ -w /usr/share/wordlists/dirbu ster/directory-list-2.3-medium.txt -o gobuster2.out -t 25
```
and we get 2 interesting locations: /feed and /upload.

The title of the machine together with the descriptions in /feed and /upload clearly suggest that we are looking at a development environment.
