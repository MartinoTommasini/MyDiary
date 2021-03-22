# My solution


How ca php check that 2 files are different and have the same md5 hash?


### Check that files are different

1. filename

Files with different filename but same content do not pass the check


2. filesize

Files with different length pass the check

3. Content
Files with same size but different content pass the check. It means that the PHP dows not only check the file size. 

We want to find 2 files that have the same md5sum but are different


### Path 1

They may have used md5(file1) == md5(file2).


https://stackoverflow.com/questions/40361567/manipulate-bypass-md5-in-php


```
> php -r 'var_dump(md5_file("file5.pdf") == md5_file("file6.pdf"));'

bool(false)
```

Find a file with a numeric string as hash
```
> echo hellohae > file6.pdf ; md5sum file6.pdf 

2e58354322002c453c96caae096aaab5  file6.pdf
```
Now see what is the integer value after juggling:
```
> php -r 'echo (int)"2e58354322002c453c96caae096aaab5";'

0
```

Find another file whose md5 hash is 0 when casted to a int.

I don't think that this path is viable because i need both md5 to be numerical strings (i.e. string in the form '2e728192719271927'). Impossible that a md5 hash gives me 2 numerical strings.



