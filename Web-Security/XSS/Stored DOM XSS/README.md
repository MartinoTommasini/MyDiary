# Stored DOM XSS

## Description

Link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored

>![](imgs/20210628-002830.png)


## Writeup

A comment feature is implemented within each post in the page

>![](imgs/20210628-012711.png)

We can test each field for XSS, starting with the simple `<script>alert(1)</script>`.

>![](imgs/20210628-003548.png)

Some filtering is in place.

We can study the source code of the page to see whether the escaping is performed client side.  
Something interesting pops up:

>![](imgs/20210628-005710.png)

Zooming into the javascript file we can analyze the code: Some HTML characters are escaped

>![](imgs/20210628-010104.png)

And this is what the function `escapeHTML` does

>![](imgs/20210628-010145.png)

It sanitizes the characters `<` and `>` by using the `replace()` function. However such function will only replace the first instance of the value.

We can easily bypass the escaping by prepending  `<>` to our payload.

However `<> <script>alert(1)</script>` doesn't seem to work.  
At this point we can try a bunch of different payloads and see whether the XSS is triggered or not.

Payload `<><img src=q onerror=alert(1)>` is successful.

>![](imgs/20210628-011129.png)

