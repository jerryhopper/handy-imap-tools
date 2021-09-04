import datetime
import time
import argparse
import os


def do_stuff():
    d = datetime.datetime.now()
    print(d)
    time.sleep(10)




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




# Set the previous month to ZERO, so it always runs when started.
prevmonth=0
# Endless loop
while True:
    # get the current datetime
    d = datetime.datetime.now()
    # Run only on the first minute of the new month
    if d.strftime("%H:%M") == "00:00" and d.strftime("%m") > prevmonth:
        do_stuff()
        # set the previous month to current.
        prevmonth=d.strftime("%m")
    # wait a second
    time.sleep(1)

