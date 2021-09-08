#!/usr/bin/python3


import datetime
import argparse
import json
import time
from datetime import tzinfo
import os,sys
import logging
from imap_tools import MailBox
from datetime import datetime
from pygelf import GelfTcpHandler, GelfUdpHandler, GelfTlsHandler, GelfHttpHandler
import logging
import requests
import html2text


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



def logEmail(msg,gelf_url ):

    plaintext = msg.text
    if len(msg.text)<8:
        h = html2text.HTML2Text()
        h.ignore_links = True
        plaintext = h.handle(msg.html)+" -  [HTML2TEXT]"


    #            "full_html_message": msg.html,

    json = {"_uid": msg.uid ,
            "source": "mailbox2graylog.py",
            "_from": msg.from_,
            "_to": msg.to,
            "timestamp": msg.date.timestamp(),
            "_date_str": msg.date_str,
            "short_message": msg.subject,
            "full_message": plaintext,
            "_from_values": msg.from_values,
            "_to_values": msg.to_values,
            "_cc_values": msg.cc_values,
            "_bcc_values": msg.bcc_values,
            "_reply_to_values": msg.reply_to_values
            }
    # POST TO GRAYLOG HTTP
    r = requests.post(gelf_url, json=json)
    print(str(r.status_code)+" "+msg.date_str+" - "+msg.subject)


def logAndDelete(mailbox ,mailbox_user, mailbox_password,gelf_url,delete):
    # get list of email subjects from INBOX folder
    with MailBox('outlook.office365.com').login(mailbox_user, mailbox_password) as mailbox:
        try:
            for msg in mailbox.fetch():
                logEmail(msg,gelf_url)
                if delete == True:
                    mailbox.delete(msg.uid)
                time.sleep(1)
        except:
            print("mailbox.fetch ERROR")
            print(sys.exc_info()[0])
            print(sys.exc_info())

            pass


# Set the previous minute to ZERO, so it always runs when started.
prevminute=0
# Endless loop
print("start mailbox2graylog.py")
while True:
    # get the current datetime
    d = datetime.now()
    # Run only on the first minute of the new month
    if d.strftime("%M") != prevminute:
        logAndDelete("INBOX",mailbox_user, mailbox_password,gelf_url,delete)
        # set the previous month to current.
        prevminute=d.strftime("%M")
    # wait a second
    time.sleep(1)
