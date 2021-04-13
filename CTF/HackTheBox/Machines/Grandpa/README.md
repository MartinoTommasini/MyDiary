# Solution

Initial nmap scan

```
nmap -sC -sV -oN nmap-initial 10.10.10.14
```

Only port 80 is open. We browse it and we see that the  website is under construction.  
Meanwhile I run gobuster to scan for hidden directories.  
```
gobuster dir -u http://10.10.10.14 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 30
```

We find the directory named "\_private" but it is not accessible because we don't have the right permissions.

We search for vulnerabilities in the web server:
```
searchsploit IIS 6.0
```
We found that it can be vulnerable to authentication bypass. That is exactly what we need.  
While looking for exploits we also bumped into an overflow that allows remote execution. The script is available on metasploit. We go in this direction since it's more comfortable.
```
use windows/iis/iis_webdav_scstoragepathfromurl
```
We set the options, the payload and we run the exploit. It works and we have a shell.  

```
meterpreter > sysinfo
Computer        : GRANPA
OS              : Windows .NET Server (5.2 Build 3790, Service Pack 2).
Architecture    : x86
System Language : en_US
Domain          : HTB
Logged On Users : 2
Meterpreter     : x86/windows
```
In "Documents and settings" we see the 2 users we are interested in (Harry and Administrator). However we don't have the privileges to acces the directories ... yet.  
We also run into some errors when we try to execute commands such as "getuid", "getprivs".

From a fast google search we found out that Windows -NET Server 5.2.3790 is vulnerable to CVE-2014-4076 (which is the same as the microsoft ms14_070 ).  
The exploit is also available in metasploit:
```
use windows/local/ms14_070_tcpip_ioctl
```
We set the options and run it. The script, unexpectedly, doesn't work. It may be due to the insufficient privileges that we have with the current account.  
We migrate to another process that has different privileges (NT AUTHORITY\NETWORK SERCICE)  
We now run the exploit again and it works. We successfully escalated our privileges to SYSTEM.  
We can now retrieve the flag files from the Desktops of Harry and Administrator.
