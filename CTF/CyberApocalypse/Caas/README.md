
# Solution

Input passed to the backend, used as parameter for the Command model.

```php
class CommandModel
{
    public function __construct($url)
    {
        $this->command = "curl -sL " . escapeshellcmd($url);
    }

    public function exec()
    {
        exec($this->command, $output);
        return $output;
    }
}
```

Input is escaped using the *escapeshellcmd()* function, then curl command is executed.  

Reference :  
1. https://github.com/kacperszurek/exploits/blob/master/GitList/exploit-bypass-php-escapeshellarg-escapeshellcmd.md#known-bypassesexploits
2. https://gtfobins.github.io/gtfobins/curl/

Use curl arguments to exfiltrate the flag somehow 

Tried:
- `http://127.0.0.1/ -F "console-output=</etc/passwd"`. Trying to dump password file and print it to stdout. Not working.
- `http://127.0.0.1/../../../../../etc/passwd`.   Nope.

This actually works in locale. It creates a request and embeds the content of /etc/passwd to the server
`curl -sL http://127.0.0.1 -F "prova=</etc/passwd"`


### Solution
Easier than what i was looking for.

We have data exfiltration on the server. File read command is 
```
curl -sL file://127.0.0.1/etc/passwd`
```

Thus our input is `file://127.0.0.1/etc/passwd`.  
We actually get the content of the */etc/passwd* file.


To get the flag:
`file://127.0.0.1/flag`

flag: `CHTB{f1le_r3trieval_4s_a_s3rv1ce}`

