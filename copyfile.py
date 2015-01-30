#!/usr/bin/env python
'''

Author: Prerana Haridoss
deffield: created: 2015-Jan-16

'''

import os
import shutil
import subprocess
import time 
import multiprocessing
import logging
import logging.handlers
import datetime
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)

def setup_logger(DataBackup):
	handler = logging.handlers.RotatingFileHandler(os.path.join(DataBackup,'copyfile.log'),\
                                                   maxBytes=1000000,backupCount=5)
    	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    	handler.setFormatter(formatter)
    	logger.addHandler(handler)

	
def check_usb(DataBackup):
	df = [s.split() for s in os.popen("df -h").read().splitlines()][1:]
	initial_length =  len(df)
        while(1):
	    try:
		df_new = [s.split() for s in os.popen("df -h").read().splitlines()][1:]
                if len(df_new) > initial_length:
                        time.sleep(3)
			abt_usb = df_new[-1]
			if len(abt_usb) > 6:
				logger.info("usb detected is: {usb}".format(usb = abt_usb))
				abt_usb[5] = " ".join(abt_usb[5:])
				del abt_usb[6:]
                        go_to_usb_dir(abt_usb[-1],DataBackup,time.ctime())
                if len(df_new) != initial_length:
                        initial_length = len(df_new)
	    except Exception,e:
		logging.exception("error while checking for usb: {error}".format(error = e))
		

def go_to_usb_dir(usb_dir,DataBackup,name):
		shutil.copytree(usb_dir,os.path.join(DataBackup,name))
		logger.info("Data copied from {usb} to {name}".format(usb=usb_dir,name=os.path.join(DataBackup,name)))

def main():
        path_name = os.path.dirname(__file__)                           #file_name is the name of the current directory
        DataBackup = os.path.join(path_name,'DataBackup')           	#path to the sirectory DataBackup
        if not os.path.exists(DataBackup):                            	#check if directory DataBackup exists
                os.makedirs(DataBackup)                               	#if not then create a directory DataBackup
        setup_logger(DataBackup)                                      	#Setting up logging for the file
	logger.info("Process: Detection of a new external usb device")
	check_usb(DataBackup)

if __name__=='__main__':
        main()
 

