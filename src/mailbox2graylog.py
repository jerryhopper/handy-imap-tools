#!/usr/bin/python3


from email.message import EmailMessage
import email
import imaplib
import re
import os
import sys
import logging
import base64
import email.parser
import time

import html2text
import requests
from bs4 import BeautifulSoup


import json
import argparse
import ssl
import datetime

#from socket import *
import socket

# Import my libs
from lib.tools import get_local_month
from lib.tools import getActualArchiveFolderName
from lib.tools import getArchiveFolderName

from lib.mailsrv import connect
from lib.mailsrv import folderExists
from lib.mailsrv import removeFolder
from lib.mailsrv import get_email_body

from pygelf import GelfTcpHandler, GelfUdpHandler, GelfTlsHandler, GelfHttpHandler
import logging












def logEmail( email_message, email_body,gelf_url ):
    #
    json = {"_from":email_message['From'],
            "_to":email_message['To'],
            "_date": email_message['Date'],
            "short_message": email_message['Subject'],
            "long_message": email_body
            }

    #email_message['To']
    #email_message['Subject']
    #email_message['Date']
    #get_email_body(email_message)
    #json={"short_message":"Hello there", "host":"example.org", "facility":"test", "_foo":"bar"}

    r = requests.post(gelf_url, json=json)
    r.status_code



def clear_inbox(conn, dest_folder):
    output=[]
    result = conn.uid('COPY', emailid, dest_folder)
    output.append(result)
    if result[0] == 'OK':
     result = mov, data = conn.uid('STORE',emailid, '+FLAGS', '(\Deleted Items)')
     conn.expunge()







def findAndDelete(sourceFolderName,conn,gelf_url,delete):
   #
   #print("findAndMove email from "+ sourceFolderName  )
   conn.select(sourceFolderName)

   resp, items = conn.uid("search",None, 'All')
   items = items[0].split()
   #print(items)
   for emailid in items:
    resp, data = conn.uid("fetch",emailid, "(RFC822)")
    if resp == 'OK':
     print(" ")
     #print(data)

     try:
         email_body = data[0][1].decode('utf-8')
         #print(email_body)
         email_message = email.message_from_string(email_body)

         #print('To:\t', email_message['To'])
         #print('From:\t', email_message['From'])
         print('Subject:', email_message['Subject'])
         #print('Date:\t', email_message['Date'])

         #print('Thread-Index:\t', email_message['Thread-Index'])
         logEmail(email_message, get_email_body(email_message),gelf_url )
     except:
         print( "Error decoding data." )
         logger.exception( sys.exc_info()[0] )
         print( sys.exc_info()[0] )
     else:
         #print("")
         #output = get_email_body(email_message)
         #print( output )

         #copy it
         #resp, data = conn.uid("fetch",emailid, "(RFC822)")
         #print(resp)
         #output=[]
         #result = conn.uid('COPY', emailid, destinationFolderName)

         #output.append(result)
         # delete it
         if delete == True:
           result = mov, data = conn.uid('STORE',emailid, '+FLAGS', '(\Deleted Items)')
           conn.expunge()


################################################################################################################
################################################################################################################
################################################################################################################
# Start

print("Starting mailbox2graylog.py")



#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger()

#logger.addHandler(GelfTcpHandler(host='graylog', port=9401))
#logger.addHandler(GelfUdpHandler(host='192.168.1.33', port=12203, include_extra_fields=True,debug=True))
#logger.addHandler(GelfTlsHandler(host='graylog', port=9403))
#logger.addHandler(GelfHttpHandler(host='gelf.devpoc.nl', port=12201, include_extra_fields=True))

#logger.info("mailbox2graylog.py was started.")

#try:
#    1/0
#except ZeroDivisionError as e:
#    logger.exception(e)


#############################################################################################################
# Check for commandline variables.
hasUserVars=False

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument('-mpass', '-mailbox_password', dest = 'mailbox_password', help = 'mailbox password.')
parser.add_argument('-muser', '-mailbox_user', dest = 'mailbox_user', help = 'mailbox user.')
parser.add_argument('-gelfurl', '-gelf_url', dest = 'gelf_url', help = 'gelf url incl. protocol and path')


# Parse the arguments
args = parser.parse_args()
if args.mailbox_password != None:
    mailbox_password = args.mailbox_password
    hasUserVars=True
if args.mailbox_user != None:
    mailbox_user = args.mailbox_user
    hasUserVars=True

if args.gelf_url != None:
    gelf_url = args.gelf_url
    hasUserVars=True

delete = False

# Check for environment variables
if hasUserVars==False:
    if 'MAILBOX_USER' in os.environ.keys():
        mailbox_user = os.environ['MAILBOX_USER']
        hasUserVars=True
    if 'MAILBOX_PASSWORD' in os.environ.keys():
        mailbox_password = os.environ['MAILBOX_PASSWORD']
        hasUserVars=True
    if 'GELF_URL' in os.environ.keys():
        gelf_url = os.environ['GELF_URL']
        hasUserVars=True
    if 'DELETE_MAIL' in os.environ.keys():
        if os.environ['DELETE_MAIL'] == "True":
           delete=True
        if os.environ['DELETE_MAIL'] == True:
           delete=True


if hasUserVars == False:
    print("Fatal: Missing arguments!")
    exit()
    
#############################################################################################################


print("Using mailbox ", mailbox_user )
print("logging to ", gelf_url )


# create the connection
connection = connect(mailbox_user,mailbox_password)

# Set the previous minute to ZERO, so it always runs when started.
prevminute=0
# Endless loop
while True:
    # get the current datetime
    d = datetime.datetime.now()
    # Run only on the first minute of the new month
    if d.strftime("%M") != prevminute:
        findAndDelete("INBOX",connection,gelf_url,delete)
        # set the previous month to current.
        prevminute=d.strftime("%M")
    # wait a second
    time.sleep(1)



exit()

