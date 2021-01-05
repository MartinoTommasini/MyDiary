# Solution

Same as in machine "Grandpa". Exploied in the same way.

Initial nmap scan

```
nmap -sC -sV -oN nmap-initial 10.10.10.14
```

Only port 80 is open. We browse it and we see that the  website is under construction.  

We know Microsoft IIS 6.0 is vulnerable. A metasploit script does the job for us.
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
In "Documents and settings" we see the 2 users we are interested in (Lewis and Administrator). However we don't have the privileges to acces the directories ... yet.  
We also run into some errors when we try to execute commands such as "getuid", "getprivs".

From a fast google search we found out that Windows -NET Server 5.2.3790 is vulnerable to CVE-2014-4076 (which is the same as the microsoft ms14_070 ).  
The exploit is also available in metasploit:
```
use windows/local/ms14_070_tcpip_ioctl
```
We set the options and run it. The script, unexpectedly, doesn't work. It may be due to the insufficient privileges that we have with the current account.  
We migrate to another process that has different privileges (NT AUTHORITY\NETWORK SERCICE)  
We now run the exploit again and it works. We successfully escalated our privileges to SYSTEM.  
We can now retrieve the flag files from the Desktops of Lewis and Administrator.
