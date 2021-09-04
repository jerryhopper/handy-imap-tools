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

#import html2text
#import requests

import json
import argparse
import ssl
import datetime
import time

# Import my libs
from lib.tools import get_local_month
from lib.tools import getActualArchiveFolderName
from lib.tools import getArchiveFolderName

from lib.mailsrv import connect
from lib.mailsrv import folderExists
from lib.mailsrv import removeFolder










def do_stuff(mailbox_user,mailbox_password):

    # create the connection
    connection = connect(mailbox_user,mailbox_password)




    # get current time
    d = datetime.datetime.now()
    #d = datetime.datetime(2016, 1, 29)

    # next & prev month
    nextdt = (d.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
    prevdt = (d.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)


    #get month numbers
    thismonth = str(d.strftime("%m"))
    prevmonth = str(prevdt.strftime("%m"))
    nextmonth = str(nextdt.strftime("%m"))

    #print(dt)
    print("Initialize...")


    # check if actual archive folder name exists.
    #print("check if actual archive folder name exists.")
    actualArchiveFolderName = getActualArchiveFolderName(thismonth)
    actualArchiveFolder = folderExists(actualArchiveFolderName , connection)
    #print( "actualArchiveFolder",actualArchiveFolder )


    # check if current month archive folder exists in the archive-folder
    #print("check if current month archive folder exists in the archive-folder")
    actualArchiveArchiveFolderName=getArchiveFolderName(thismonth)
    actualArchiveArchiveFolder= folderExists(actualArchiveArchiveFolderName , connection)
    #print("actualArchiveArchiveFolder",actualArchiveArchiveFolder)



    # check if past month archive folder exists in the root
    pastArchiveFolderName=getActualArchiveFolderName(prevmonth)
    #print("check if past month archive folder exists in the root ("+pastArchiveFolderName+")")

    pastArchiveFolder= folderExists(pastArchiveFolderName , connection)
    #print("pastArchiveFolder",pastArchiveFolder)


    # check if past month archive folder exists in the archive
    #print("check if past month archive folder exists in the archive")
    pastArchiveArchiveFolderName=getArchiveFolderName(prevmonth)
    pastArchiveArchiveFolder= folderExists(pastArchiveArchiveFolderName , connection)
    #print("pastArchiveArchiveFolder",pastArchiveArchiveFolder)


    ##testing##connection.create( str("\""+prevmonth + ". " + get_local_month(prevmonth) + " Archief.\"") )

    if ( actualArchiveArchiveFolder == "NO" and actualArchiveFolder == "NO" ):
       print("create current month folder!")
       # Create a new mailbox
       typ, create_response = connection.create(actualArchiveFolderName )
       print ('CREATED '+ actualArchiveFolderName  +':', create_response)
       actualArchiveArchiveFolder = "OK"


    if ( pastArchiveFolder == "OK" and pastArchiveArchiveFolder =="NO" ):
       print("We need to move folders and email *")
       # create folder
       if ( pastArchiveArchiveFolder =="NO" ):
          # create archive folder for past month!  pastArchiveArchiveFolderName
          # Create a new archived mailbox
          typ, create_response = connection.create( pastArchiveArchiveFolderName )
          print ('CREATED '+ pastArchiveArchiveFolderName +':', create_response)
       # find and move emails.
       findAndMove(pastArchiveFolderName,pastArchiveArchiveFolderName ,connection)
       # remove pastArchiveFolder
       removeFolder(pastArchiveFolderName,connection)

       return

    if ( pastArchiveFolder == "OK" and pastArchiveArchiveFolder =="OK" ):
       print("We need to move folders and email **")
       # find and move emails.
       findAndMove(pastArchiveFolderName,pastArchiveArchiveFolderName ,connection)
       # remove pastArchiveFolder
       removeFolder(pastArchiveFolderName,connection)
       return


    if ( actualArchiveFolder == "OK" ):
       print("we have nothing to do.")
       return







################################################################################################################
################################################################################################################
################################################################################################################
# Start 

print("Starting monthly-mailbox.py")

#############################################################################################################
# Check for commandline variables.
hasUserVars=False

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument('-mpass', '-mailbox_password', dest = 'mailbox_password', help = 'mailbox password.')
parser.add_argument('-muser', '-mailbox_user', dest = 'mailbox_user', help = 'mailbox user.')

# Parse the arguments
args = parser.parse_args()
if args.mailbox_password != None:
    mailbox_password = args.mailbox_password
    hasUserVars=True
if args.mailbox_user != None:
    mailbox_user = args.mailbox_user
    hasUserVars=True

# Check for environment variables
if hasUserVars==False:
    if 'MAILBOX_USER' in os.environ.keys():
        mailbox_user = os.environ['MAILBOX_USER']
        hasUserVars=True
    if 'MAILBOX_PASSWORD' in os.environ.keys():
        mailbox_password = os.environ['MAILBOX_PASSWORD']
        hasUserVars=True

if hasUserVars == False:
    print("Fatal: Missing arguments!")
    exit()
    
#############################################################################################################

print("Using mailbox ", mailbox_user )

# Set the previous month to ZERO, so it always runs when started.
prevmonth=0
# Endless loop
while True:
    # get the current datetime
    d = datetime.datetime.now()
    # Run only on the first minute of the new month
    if d.strftime("%H:%M") == "00:00" and d.strftime("%m") > prevmonth:
        do_stuff(mailbox_user,mailbox_password)
        # set the previous month to current.
        prevmonth=d.strftime("%m")
    # wait a second
    time.sleep(1)




exit()
