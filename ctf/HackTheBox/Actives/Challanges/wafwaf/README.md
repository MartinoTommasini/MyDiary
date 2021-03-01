# My solution

We browse the webpage and we get a php error which is exposed due to an error. We can take a look at the source code.  
We see the server expects as to use a POST request. However data is not accessed using $\_POST but using the file_get_contents('php://input') which returnes the raw byte data of the POST payload. It is useful used when data is presented as a JSON data. Here there are more information: https://stackoverflow.com/questions/8893574/php-php-input-vs-post.   
In this application the raw byte retrieved from the POST payload are sanitizezd using preg_match_all and than decoded as JSON. The JSON object is then used as input for a SQL query that we suspect is vulnerable to injection.

```
<?php
// Your code here!

$s = '{"user":1}';
$obj = json_decode($s);

var_dump($obj->user);
?>
```
This returns 1, so the json variable we'll use is 'user'.  
We copy the pattern of the preg_match_all in a local editor and we resolve it. In this way we can cleary see what is the pattern used for the sanitization. Namely
```
/[\(\*\<\=\>\|'&\-@]|select|and|or|if|by|from|where|as|is|in|not|having/i
```
This is an easy online resource to debug the regular expression: https://regex101.com/. It comes handy in this situation.  
The final /i stands for case insensitive match, thus using OR will not be allowed.  
Special characters that we cannot use are:
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

Let's see what we can escape

We reproduce the script in locale
```
<?php
// Your code here!
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
        echo "VSPRINTF\n";
        var_dump(vsprintf($sql, $args));
    }
}

$db = new db();

$input = '{"user": \x27\x6F\x72\x20\x27\x31\x27\x3D}';


$obj = $db->waf($input);
echo "OBJ\n";
var_dump($obj);
$db->query("SELECT note FROM notes WHERE assignee = '%s'", $obj->user);
 

?>
```

Try with sqlmap !
