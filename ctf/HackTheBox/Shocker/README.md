# Solution

Start with the usual nmap enumeration
```
>nmap -sC -sV -Pn -oN nmap-initial 10.10.10.56
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

The website just whoes an image. We use exiftool to see whether it carries some interesting metadata but no.  
We run gobuster
```
gobuster dir -u http://10.10.10.56 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 25 -o gobuster.out
```
It didn't produce interesting results.  

We run nikto
```
nikto -host 10.10.10.56 -output nikto.txt
```
We have a line that may be interesting
```
+ Allowed HTTP Methods: POST, OPTIONS, GET, HEAD
```
The OPTIONS method may give us some usefull debug informations.  
We send an OPTIONS request using burp but we don't get any new info, just the allowed methods (that we already know) and the apache version.  

No luck so far. We try to search whether apache is vulnerable somehow.  
We don't find any specific vulnerabilities on exploit DB. However the name of the machine is Shocker, so, what about a shellshoke?  
We use the nmap http-shellshock script to scan for the vulnerability
```
>nmap -sV -p80 --script http-shellshock -oN nmap-shellshock 10.10.10.56
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
```
The script does not find any shellshock vulnerabilities. We take a closer look at the script on the NMAP web page and see find the following sentence: "To detect this vulnerability the script executes a command that prints a random string and then attempts to find it inside the response body. Web apps that don't print back information won't be detected with this method. "  
It may be possible that the webserver doesn't print the result of the remote code execution on the response. We can try a blind injection and see if the shellshock actually takes place.  
We intercept a normal HTTP request to the webserver and we play with the headers.  
The attack vector used is 
```
() { :;}; ping -c 2 10.10.14.25
```
We try it as user agent and referer first, but no luck. We also try with other header fields but nope.  
We are quite sure the vulnerability is not in SSH because you'd need to authenticate for a shellshock attack to it.  
We restart with enumeration, hoping to find something new.  
We run gobuster again with a bigger dictionary
```
gobuster dir -u http://10.10.10.56 -w /usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt -t 25 -o gobuster_ext.out
```

We run niko with the shellshocke plugin
```
nikto --host 10.10.10.56 -Plugins shellshock -o nikto-shellshock.txt
```
Nothing found. I suppose the script works the same as the nmap one.

Look nikto outputs (also the standard nikto and try shellshock on those headers).
I fired up as much gobuster instances as possible. I try to fuxx with different extentions php,txt,html,sh,bash,cgi.  
To look at status codes. It  may be possible that gobuster does not log the result we want because it has a different status cde than the default ones. Therefore I use gobuster with the negative status code flag (-b 404). In this way it prints every resource it finds with status code different than 404.  


Tried:
```
gobuster dir -u http://10.10.10.56/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 20 -x cgi   -o gobuster_cgi.out
gobuster dir -u http://10.10.10.56 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 25 -x txt,php,html,bash,sh   -o gobuster_extentions.out
 ```

By looking at the shellshock in Internet, we can see that a recurrent directory is /cgi-bin. Even if this directory is listed in the dictionary file we used, we try to enter it manually (Yes, I was deserate at this point, couldn't find my way in :(  ). It magically worked.  
Why did gobuster haven't found it? Because it tried /cgi-bin which returns a 404 and not /cgi-bin/ which returns a 403. 

Now we have a new road to follow and it seems very promising.  
We can now scan inside the directory.  
