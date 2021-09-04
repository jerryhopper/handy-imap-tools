
FROM python:3.6

#RUN apk add --update --no-cache postgresql-dev gcc python3-dev musl-dev

# Add Office365 module
RUN pip3 install O365

# Add Requests module
RUN pip3 install requests

# Add Gelf module
RUN pip3 install pygelf

# Add htmltext module
RUN pip3 install html2text

# Add beautifulsoup module
RUN pip3 install beautifulsoup

# Create app dir
RUN mkdir /app

# Copy contents
COPY ./src /app

# Set workdir
WORKDIR = "/app"

#CMD [ "python", "/app/monthly-mailbox.py" ]
