#!/usr/bin/env python
'''

Author: Prerana Haridoss
Copyright: 2015 IISC, Bangalore. All rights reserved.
deffield: created: 2015-Jan-16

'''

import os
import shutil
import re
import requests
import subprocess
import socket
import time 
import multiprocessing
import json
import logging
import logging.handlers
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)

def setup_logger(JJDataBackup):
	handler = logging.handlers.RotatingFileHandler(os.path.join(JJDataBackup,'copyfile.log'),\
                                                   maxBytes=1000000,backupCount=5)
    	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    	handler.setFormatter(formatter)
    	logger.addHandler(handler)


def open_copy_file(JJDataBackup,read_file_pipe):
    while(1):
	try:
		if read_file_pipe.poll() == True:
			backup_file = read_file_pipe.recv()[0]
			f = open(backup_file,'r')
			Data = f.read()
			f.close()
			Data = Data.splitlines()
			Data = json.dumps(Data)
			done = False
			while(done == False):
				done = send_file(Data, done)
				if done == True: os.remove(backup_file)
	except Exception,e:
		logger.exception("error while opening and coping file:{e}".format(e = e))
	
	
def send_file(Data,done):
	url = "http://localhost:8080/jjdata"
	headers = {'content-type' : 'application/json'}
	try:
			r = requests.post(url,data = Data, headers=headers)	
			if r.status_code == 200:
				logger.info("STATUS CODE: 200 Data is successfully sent")
				done = True
	except:
		done = False
	return done
	
def check_usb(JJDataBackup,usb_detected_pipe):
	files_in_JJDatabackup = os.listdir(JJDataBackup)
	for files in files_in_JJDatabackup:
		if files.endswith('D.TXT'): usb_detected_pipe.send([os.path.join(JJDataBackup,files)])
		logger.info("files in JJDataBackup are being sent for uploading")
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
				abt_usb[5] = abt_usb[5]+' '+abt_usb[6]
				del abt_usb[6]
                        go_to_usb_dir(abt_usb[-1],usb_detected_pipe,JJDataBackup)
                if len(df_new) != initial_length:
                        initial_length = len(df_new)
	    except Exception,e:
		logging.exception("error while checking for usb: {error}".format(error = e))
		

def go_to_usb_dir(usb_dir,usb_detected_pipe,JJDataBackup):
                file_name = os.path.dirname(__file__)
                files = os.listdir(usb_dir)
                if 'CONFIG.TXT' in files:
                        #config_file = open(os.path.join(usb_dir,'CONFIG.TXT'),'r')
                        #content = config_file.read()
                        #config_file.close()
                        #match = re.search('www.commonsensenet.in',content,re.I|re.M)
                        #if match:
                                logger.info("There is a CONFIG.TXT file and it is the correct CONFIG.TXT file")
                                for al in files:
                                        if al.endswith('D.TXT'):
                                                shutil.copy(os.path.join(usb_dir,al),JJDataBackup)
                                                logger.info("the contents on a -D.TXT file has been copied into the local directory")
                                                usb_detected_pipe.send([os.path.join(JJDataBackup,al)])
                                        else: continue
                else: pass

def main():
        usb_detected_pipe , read_file_pipe = multiprocessing.Pipe()     #function returns a pair of connection objects connected by a pipe which by default is duplex (two-way)
        file_name = os.path.dirname(__file__)                           #file_name is the name of the current directory
        JJDataBackup = os.path.join(file_name,'JJDataBackup')           #path to the sirectory JJDataBackup
        if not os.path.exists(JJDataBackup):                            #check if directory JJDataBackup exists
                os.makedirs(JJDataBackup)                               #if not then create a directory JJDataBackup
        setup_logger(JJDataBackup)                                      #Setting up logging for the file
        p1 = multiprocessing.Process(target = check_usb,args = (JJDataBackup,usb_detected_pipe,))
        p1.start()                                                      #starting one process
        logger.info("first process has started: Detection of a new external usb device")
        p2 = multiprocessing.Process(target = open_copy_file,args = (JJDataBackup,read_file_pipe,))
        p2.start()                                                      #starting second process
        logger.info("second process which sends file contents to the server has been started")
        p1.join()
        p2.join()

if __name__=='__main__':
        main()
 

