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
3.  Acces /console or trigger internal server error to make the console show up
https://medium.com/swlh/hacking-flask-applications-939eae4bffed

The more promising so far is tryng to trigger an internal server error.

### Path 1: Trigger internal state 

1. Change values of os in the payload field  
Since the user is limited to select the values linus,windows or android,  the back end may give the selection of one of this 3 possibilities for granted. We thus try to modify the http payload with Burp, hoping to cause an internal error in the server.  
We tried with names such as 'lll' or also special charachters as \',\",\*. Invalid os is returned by the back end.  
2. Trigger internal state error by using a malformed msfvenom template file  
Did not yield to any results

### Path 2: Command injection in msfvenom template file
While googling for information regarding the template file and msfvenom, we run into the CVE-2020-7384: Malicious user may upload a malicious template file in msfvenom which would trigger code execution on the target machine.  
Metasploit created a module for this vulnerability as we can see from the metasploit github page: https://github.com/rapid7/metasploit-framework/pull/14331.  

We thus use metasploit to exploit the vulnerability.  
We select the module, modify the options and we run the exlpoit. This will generate the apk file containing our command injection that will be executed by msfvenom on the target machine.  
We start a exploit/multi/handler on our host mahcine and upload the generated apk file in the specific form in the web server. The os which has to be selected is android, the ip can be an arbitrary one instead.  

Once we press *generate* a reverse shell will be started on the metasploit handler instance.  
In order to have a nicer shell, we can try to upgrade from a netcat to meterpreter shell.  
We use the module multi/manage/shell_to_meterpreter and get a meterpreter shell. The user flag is under /home/kid.  

We now want to escalate the privileges


