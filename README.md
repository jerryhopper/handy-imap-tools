# handy-imap-tools

These tools were made while using office365. the problem was that many users use a shared mailbox, and the mailbox-archive became huge and badly searchable due to syncing with many clients.
For this a mailbox-archive protocol was used. In practice this means the archive mailbox would have subdirectories per month, and we limit this to 12 subdirectories.

Obviously, these tasks can be automated.


## monthly-archive

this script should be run at 00:00 of day 1 of a new month. it creates month-folders in archive mailbox, and creates a 'current month archive' mailbox, and moves the past-month's folder to the mailbox=archive. 
 

## mail-to-graylog

this script should run every X minutes. it parses the mailbox and logs them to a graylog instance. after logging - the email gets deleted.  By using graylog, the large mail-archive is searchable due to the graylog extractors which consolidate important data from email body.
Because the office365 mailbox is not consistent in its search results due to the sync problems, graylog provides a simple interface to search the logged emails.

