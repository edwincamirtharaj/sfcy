# views.py

from django.shortcuts import render
from .management.commands.fetch_emails import Command as FetchEmailCommand  # Correct import path

def show_emails(request):
    # Call the management command to fetch email data
    fetch_email_command = FetchEmailCommand()
    emails_data = fetch_email_command.handle()

    # Render the template with the email data
    return render(request, 'emails_template.html', {'emails_data': emails_data})
