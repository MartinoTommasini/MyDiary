# My solution

Start with usual nmap enumeration 
```
nmap -sC -sV -oN nmap-initial 10.10.10.222
```


Port 22 and 80 open where an nginx server is listening.  
We visit the service on port 80 and the page contains links to 2 different domain name, namely helpdesk.delivery-htb and delivery.htb. We add them in our /etc/hosts file so that we can access them.

Paths:
1. Get email/username in helpdesk and recover account in Mattermost server
2. get username and password in helpdesk server
3. Get @delivery.htb in helpdesk ans use it to login to mattermost server

We run dirbuster on both delivery.htb:80 and helpdesk.delivery.htb


We are told that we can modify our ticket by sending an email at the support team:
8439402@delivery.htb


1. Try to register a delvery.htb account and hope it works for the mattermost server.  
We registered an account in helpdesk server as:
mail: kevin@delivery.htb
name: kevin
password: kevindelivery  

Once you registered for an account you are not allowed to sign in or see open tickets untill you confirm the registration. However the confirmation email never arrives.  
You can instead see open tickets even if you are not registered. It automatically logs in as giest user after you create a ticket.

Path 1. does not work

2. 

We go in helpdesk.delivery.htb and we open a ticket as luca@gmail.com.
TIcket id= 9224074

This is the response we receive after opening the ticket:
```
luca, 

You may check the status of your ticket, by navigating to the Check Status page using ticket id: 9224074.

If you want to add more information to your ticket, just email 9224074@delivery.htb.

Thanks,

Support Team
```

We have a valid email with domain delivery.htb. 

3. Mess around with the api
From the results od dirbuster we see that the helpdesk.delivery.htb website has a /api/ directory.  
The website is powered by OsTicket, we can thus take a look at what it is and what is the api it uses.  
The access to the api may be useful to execute unrestricted operations. 

Ipothesis:
- Recover password of the account and use it to login to mattermost server
- Interact with the mail server and login
- Interact with api since we found a /api/ in dirbuster. 
- XSS in email: using email <script>alert("antonio")</script>@gmail.com
- Add a forwarding rule in pipe.php. From 9224074@delivery.htb to my personal email. Then recover the password in mattermost server
- Code injection in email forwarded to php script


Next time:
- ook better at documentation of API. IN particular cron.php and piping
- source code of osTicket: https://github.com/osTicket/osTicket/releases/tag/v1.15.2

start by reading everything again, and try to see if i can get the confirmation email back
