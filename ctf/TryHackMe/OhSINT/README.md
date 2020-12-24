# OhSINT

What information can you possible get with just one photo ?

![Picture](WindowsXP.jpg)

## Solution

We can use exiftool to read the metadata info in the picture.  
If not already installed:
```
sudo apt install libimage-exiftool-perl
```

Execution of exiftool
```
> exiftool WindowsXP.jpg
ExifTool Version Number         : 12.09
File Name                       : WindowsXP.jpg
Directory                       : .
File Size                       : 229 kB
File Modification Date/Time     : 2020:11:08 16:52:42+01:00
File Access Date/Time           : 2020:11:08 16:55:32+01:00
File Inode Change Date/Time     : 2020:11:08 16:52:56+01:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
XMP Toolkit                     : Image::ExifTool 11.27
GPS Latitude                    : 54 deg 17' 41.27" N
GPS Longitude                   : 2 deg 15' 1.33" W
Copyright                       : OWoodflint
Image Width                     : 1920
Image Height                    : 1080
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 1920x1080
Megapixels                      : 2.1
GPS Latitude Ref                : North
GPS Longitude Ref               : West
GPS Position                    : 54 deg 17' 41.27" N, 2 deg 15' 1.33" W
```
We can extract the author of the picture from the Copyright tag.  
From a gooogle search we find the avatar of Owoodflint's twitter account -> a cat :)


Using google maps and the GPS coordinates we have, we see that the location is close to a city named Hawes. 
However, it's not the correct one, since TryHackMe doesn't accept the solution.

Again,with a simple google search we can find the email address and the city in his [github repo](https://github.com/OWoodfl1nt/people_finder/blob/master/README.md):  
OWoodflint@gmail.com  
London

Alternatively, we can use Wingle.net to find the Location. The author posted the BSSID of his access point on twitter ( B4:5D:50:AA:86:41 ). Feeding the BSSID as input we get the location and the SSID of the access point.

In his [blog](https://oliverwoodflint.wordpress.com/2019/03/03/the-journey-begins/)  we discover that he has been in New York for the holidays

As last thing, we need to find his password. *Have I been Pwned*  does not identify any breach linked with his mail account.  
I didn't nothis this in the first place but some the password is embedded in one of the previous links. In the source code of the Blog page, we see the password. It had the same color of background.
```html
<p style="color:#ffffff;" class="has-text-color" data-adtags-visited="true">pennYDr0pper.!</p>
```
