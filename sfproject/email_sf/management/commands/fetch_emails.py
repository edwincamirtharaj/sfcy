# email_sf/management/commands/fetch_emails.py

import imaplib
import email
from email.header import decode_header
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import re
import pytz # need to install

class Command(BaseCommand):
    help = 'Fetch all emails received in Gmail using IMAP'

    def handle(self, *args, **options):
        # Gmail IMAP server settings
        imap_server = 'imap.gmail.com'
        imap_port = 993

        # Your Gmail credentials
        username = 'sfconsultancyservices@gmail.com'
        password = 'dprd yjls cila ofud'

        # Email address to filter by
        filter_email = 'donotreply@gst.gov.in'  # Change this to the desired email address

        # Connect to the Gmail IMAP server
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)

        # Login to your Gmail account
        mail.login(username, password)

        # Select the mailbox (inbox in this case)
        mail.select('inbox')

        # Calculate the date 2 days ago
        date_2_days_ago = (datetime.now() - timedelta(days=2)).strftime('%d-%b-%Y')

        # Search for emails from the specified email address since 2 days ago
        _, messages = mail.search(None, '(FROM "{}" SINCE "{}")'.format(filter_email, date_2_days_ago))
        messages = messages[0].split()

        emails_data = []  # List to store email data

        for msg_id in messages:
            # Fetch the email
            _, msg_data = mail.fetch(msg_id, '(RFC822)')
            raw_email = msg_data[0][1]

            # Parse the raw email using the email library
            msg = email.message_from_bytes(raw_email)
            
            email_date = msg['Date']

            # Extract email headers
            subject = decode_header(msg['Subject'])[0][0]
            sender = decode_header(msg['From'])[0][0]
            message_id = msg['Message-ID']
            message_id = message_id.strip('<>')
            
            # Remove timezone information and any leading/trailing whitespace from the date string
            email_date = re.sub(r'[\W_]+', ' ', email_date).strip()
            # Split the date string to separate the timezone information
            date_parts = email_date.split()
            # Join the date parts except the last two (which represent the timezone)
            date_string = ' '.join(date_parts[:-2])
            # Parse the date string into a datetime object
            email_date_time = datetime.strptime(date_string, '%a %d %b %Y %H %M %S')
            # Extract the timezone offset from the last two parts of the date string
            timezone_offset_hours = int(date_parts[-2]) // 100
            timezone_offset_minutes = int(date_parts[-2]) % 100
            # Create a timedelta object for the timezone offset
            timezone_offset = timedelta(hours=timezone_offset_hours, minutes=timezone_offset_minutes)
            # Adjust the datetime object with the timezone offset
            email_date_time += timezone_offset
            # Set the timezone to IST
            email_date_time = email_date_time.replace(tzinfo=pytz.timezone('Asia/Kolkata'))

            # Initialize variables to store email body
            email_body = ''

            # Process the email payload
            if msg.is_multipart():
                # Iterate over email parts
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    # Extract text content from HTML or plain text parts
                    if "attachment" not in content_disposition:
                        payload = part.get_payload(decode=True)  # Get the payload
                        if payload is not None:  # Check if payload is not None
                            body = payload.decode()  # Decode the payload
                            email_body += body
            else:
                # Extract text content from single-part email
                payload = msg.get_payload(decode=True)  # Get the payload
                if payload is not None:  # Check if payload is not None
                    email_body = payload.decode()  # Decode the payload

            # Store email data in a dictionary
            email_data = {
                'subject': subject,
                'sender': sender,
                'date_time': email_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                'body': email_body,
                'message_id': message_id
            }

            emails_data.append(email_data)  # Append email data to the list
            
        # Sort emails_data based on the date_time in descending order
        emails_data = sorted(emails_data, key=lambda x: datetime.strptime(x['date_time'], '%Y-%m-%d %H:%M:%S'), reverse=True)

        # Close the connection
        mail.close()
        mail.logout()

        return emails_data  # Return the list of email data