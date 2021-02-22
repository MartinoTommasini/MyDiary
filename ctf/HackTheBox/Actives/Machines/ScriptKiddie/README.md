# My solution

Start with usual nmap script to enumerate.  
```
nmap -sC -sV -oN nmap-initial 10.10.10.226
```

We see ssh open, a fitered 903 port and a webserver on 5000.  
We start by looking at port 5000. As we see from the nmap outcome, port 5000 hosts a Werkzeug web application which uses python 3.8.5

Run dirbuster: http://10.10.10.226:5000/, not recursive, extentions: py,html, dictionary medium

Interesting:
1. May contain sensitive information ?
http://10.10.10.226:5000/static/hacker.css
2. fuzz url to find console 
e.g. http://10.10.10.226:5000/$FUZZ$/console
3.  Acces /console or trigger internal server error to make the console show up
https://medium.com/swlh/hacking-flask-applications-939eae4bffed
