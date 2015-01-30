OBJECTIVE
--------------------------------------------------------
Simple script to copy files from an external USB drive to 
a local directory automatically. Two ways to use this script:

USAGE
-------------------------------------------------------
1. run the script in background by putting in the crontab
$crontab -e
insert: @reboot python </path to the file/>&

For example:	if the path to the file is /home/person/Desktop/copyfile.py
		then insert: @reboot python /home/person/Desktop/copyfile.py&	  

2. run the script as and when required.
For example:	$python /home/person/Desktop/copyfile.py #add an & to run the script in the background.

RESULT
------------------------------------------------------
The files will get stored in the place where you run the script. 
For example:	if the path to the file is /home/person/Desktop/copyfile.py
		then the files with store in the directory /home/person/Desktop/DataBackup



