

from email.message import EmailMessage
import email
import imaplib
import re
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



# function that returns Localized monthname based on month-number
def get_local_month(month):
   if month == "01":
      return "Januari"
   if month == "02":
      return "Februari"
   if month == "03":
      return "Maart"
   if month == "04":
      return "April"
   if month == "05":
      return "Mei"
   if month == "06":
      return "Juni"
   if month == "07":
      return "Juli"
   if month == "08":
      return "Augustus"
   if month == "09":
      return "September"
   if month == "10":
      return "Oktober"
   if month == "11":
      return "November"
   if month == "12":
      return "December"




# function that returns the archive-folder name (ROOTFOLDER)
def getActualArchiveFolderName(month):
   return str("\""+month + ". " + get_local_month(month) + " Archief.\"")


# function that returns the archive-folder name (ARCHIVEFOLDER)
def getArchiveFolderName(month):
   #
   return str("\"Archief/"+month + ". " + get_local_month(month) + " Archief.\"")
