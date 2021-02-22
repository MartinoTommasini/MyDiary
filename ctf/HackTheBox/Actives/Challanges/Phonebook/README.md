

Search phonebook entry at http://104.248.168.9:30736/964430b4cdd199af19b986eaf2193b21f32542d0/  
However access is denied and queries do not compete succesdfully

New (9.8.2020): You can now login using the workstation username and password! - Reese

We try to log in with random credentials and we study the interaction using Burp.  
We see that when a invalid credential is entered, a first POST request to the login entry is generated as expected  .  
The responses forces the client to a GET request to the following reative path "/login?message=Authetication failed". The message is then displayed back to the client.  

As the message is displayed back we want to see if it is vulnerable to XSS. We can try to see if the message variable is vulnerable to XSS
```
http://104.248.168.9:30736/login?message=<h1>hello</h1>
```
The hello message is displayed in bold, thus confirming our first idea.  
Let's see what we can do from here


LDAP injection. Possible to enumerate username and password.
The difficult part of the challange was to realize what was the vulnerability in question. Once the LDAP vulnerability is detected, a simple python script does the job. The password of the user is the flag.  

