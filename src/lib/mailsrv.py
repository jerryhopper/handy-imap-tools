

from email.message import EmailMessage
import email
import imaplib
import re
import sys
import logging
import base64
import email.parser

import html2text
#import requests

import json
import argparse
import ssl
import datetime

#import lib.getemailbody 


# function that creates the connection.
def connect(user,mailbox_password):
   # Load system's trusted SSL certificates
   tls_context = ssl.create_default_context()
   conn = imaplib.IMAP4("outlook.office365.com")
   conn.starttls(ssl_context=tls_context)
   conn.login(user,mailbox_password)
   return conn




# function that checks if mailbox-folder exists.
def folderExists(folder,conn):
   code = conn.select(folder)
   #print("folderExists",code)
   return code[0]



def removeFolder(folderName,conn):
    # ....
    conn.select("INBOX")
    print("Remove Folder "+ folderName)
    result = conn.delete(folderName)
    print(result)



## unused function
def findAndMove(sourceFolderName,destinationFolderName,conn):
   #
   print("findAndMove email from "+ sourceFolderName + " to "+ destinationFolderName )
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
         subject = email_message["Subject"]

         #print('To:\t', email_message['To'])
         #print('From:\t', email_message['From'])
         print('Subject:', email_message['Subject'])
         print('Date:\t', email_message['Date'])
         #print('Thread-Index:\t', email_message['Thread-Index'])
     except:
         print( "Error decoding data." )

     else:
         #print(subject)
         #output = get_email_body(email_message)
         #print( output )

         #copy it
         resp, data = conn.uid("fetch",emailid, "(RFC822)")
         print(resp)
         output=[]
         result = conn.uid('COPY', emailid, destinationFolderName)

         output.append(result)
         # delete it
         if result[0] == 'OK':
          result = mov, data = conn.uid('STORE',emailid, '+FLAGS', '(\Deleted Items)')
          conn.expunge()
