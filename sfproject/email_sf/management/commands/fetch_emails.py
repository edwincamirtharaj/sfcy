# email_sf/management/commands/fetch_emails.py

import imaplib
import email
from email.header import decode_header
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fetch all emails received in Gmail using IMAP'

    def handle(self, *args, **options):
        # Gmail IMAP server settings
        imap_server = 'imap.gmail.com'
        imap_port = 993

        # Your Gmail credentials
        username = 'sfconsultancyservices@gmail.com'
        password = 'Sfcy@2021'

        # Connect to the Gmail IMAP server
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)

        # Login to your Gmail account
        mail.login(username, password)

        # Select the mailbox (inbox in this case)
        mail.select('inbox')

        # Search for all emails
        status, messages = mail.search(None, 'ALL')
        messages = messages[0].split()

        emails_data = []  # List to store email data

        for msg_id in messages:
            # Fetch the email
            status, msg_data = mail.fetch(msg_id, '(RFC822)')
            raw_email = msg_data[0][1]

            # Parse the raw email using the email library
            msg = email.message_from_bytes(raw_email)

            # Extract email headers
            subject = decode_header(msg['Subject'])[0][0]
            sender = decode_header(msg['From'])[0][0]

            # Store email data in a dictionary
            email_data = {
                'subject': subject,
                'sender': sender,
            }

            emails_data.append(email_data)  # Append email data to the list

        # Close the connection
        mail.close()
        mail.logout()

        return emails_data  # Return the list of email data
