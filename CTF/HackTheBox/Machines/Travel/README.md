# Solution

I watched the Ippsec writeup video before trying it on my own. This is not thus my personal solution. 
Once watched the video, I tried to solve it on my own.  

1. Start with usual nmap enumeration

2. 3 different domains for 10.10.10.189

3. Found directory .git in blog-dev.travel.htb. It contains a git repository

4. Dump the git repository with git-dumper

5. Looking at the read me we know that rss_template.php and template.php are in http://blog.travel.htb/wp-content/themes/twentytwenty/

6. We study the php codes to see whether we can find any kind of vulnerabilities

7.
