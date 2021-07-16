# Micro-CMS v1

There are 4 flags (= at least 4 vulnerabilities) in this website. We need to hunt them all.

The landing page is :

>![](imgs/2021-07-15-11-46-28.png)


We can create our own page using Markdown.

## Flag 1 - Stored XSS on Title 

An XSS in the `Title` input:

>![](imgs/2021-07-15-11-48-28.png)

## Flag 2 - Stored XSS on Body

The `<script>alert(1);<script>` is filtered in the page body.  
However we can use the `<img>` tag and trigger the XSS:

>![](imgs/2021-07-15-11-50-31.png)

## Flag 3 - Broken access control

We notice that the posts we create are indexed sequentially starting from 10. The indexes between 3 and 9 (included) are not used. This is indeed a strange behavior.

So, we try to access those indices using `ffuf`

>![](imgs/2021-07-15-21-24-03.png)

As we can see, we get a weird 403 for the index 7,namely `http://35.190.155.168/eed29828c5/page/7`

Since we are forbidden the access to such resource, we can try to check whether we can access it in other ways.  

The website offers the possibility to edit previously created pages. So we can try to edit the page at index 7 by visiting the page `/eed29828c5/page/edit/7`. 

The access to the resource is not forbidden this time and we there we find our flag

>![](imgs/2021-07-16-10-20-44.png)


## Flag 4 - Tweaking url inputs

We try to think about the url inputs that may not be hardcoded in the web app.

Since the page ID may be one of those, we try to replace the expected integer with a special character.

We surprisingly get the flag when we provide a single quote `'`. 

>![](imgs/2021-07-16-10-12-32.png)

Probably the application is crashing due to SQL injection and prints the flag to the page as error.