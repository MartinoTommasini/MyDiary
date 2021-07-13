# CSRF with no defenses in place

## Description

Link: https://portswigger.net/web-security/csrf/lab-no-defenses

>![](imgs/2021-07-13-13-02-06.png)


## Writeup

We can login to our account with the credentials we have `wiener:peter`.

Once logged it we are redirected to our account page

>![](imgs/2021-07-13-15-34-46.png)

Here we can change our email by providing a new email.

We fire up Burp in order to record the `update email` request and analyze it

>![](imgs/2021-07-13-15-50-31.png)

The new email is specified in the POST body and url encoded. 

Since there aren't any CSRF protections we can simply make the victim issue a `change email` operation and hardcode the new email in the post body. 

The response that we will serve back to the victims when they visit the `/exploit` page is the following:

>![](imgs/2021-07-13-16-03-53.png)

The form will be submitted without any user interaction and they email will be changed to **pwned@gmail.com**.

The CSRF attack succedeed.