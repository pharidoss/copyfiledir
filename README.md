OBJECTIVE
--------------------------------------------------------
Simple script to copy files from an external USB drive to 
a local directory automatically. Two ways to use this script:

USAGE
-------------------------------------------------------
1. run the script in background by putting in the crontab
<pre style="white-space: pre-wrap; 
white-space: -moz-pre-wrap; 
white-space: -pre-wrap; 
white-space: -o-pre-wrap; 
word-wrap: break-word;">
$crontab -e
</pre>
insert: 
<pre style="white-space: pre-wrap; 
white-space: -moz-pre-wrap; 
white-space: -pre-wrap; 
white-space: -o-pre-wrap; 
word-wrap: break-word;">
@reboot python [path to the script] &
</pre>


2. run the script as and when required.

<pre style="white-space: pre-wrap; 
white-space: -moz-pre-wrap; 
white-space: -pre-wrap; 
white-space: -o-pre-wrap; 
word-wrap: break-word;">
$python /home/person/Desktop/copyfile.py #add an & to run the script in the background.
</pre>

RESULT
------------------------------------------------------
The files will get stored in the place where you run the script. 
For example:	if the path to the file is /home/person/Desktop/copyfile.py
		then the files with store in the directory /home/person/Desktop/DataBackup



