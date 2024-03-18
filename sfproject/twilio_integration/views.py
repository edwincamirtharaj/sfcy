# views.py
import os
from django.shortcuts import render
from django.conf import settings
from twilio.rest import Client
from company.models import WhatsAppNumber

from django.http import HttpRequest, HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt

import json
import logging

logger = logging.getLogger(__name__)

def success_view(request):
    return render(request, 'twilio_integration/success.html')


@csrf_exempt
def handle_whatsapp_message(request: HttpRequest):
    # Extract data from Twilio request
    incoming_message = request.POST.get('Body', '')
    sender_whatsapp_number = request.POST.get('From', '')

    cleaned_number = ''.join(c for c in sender_whatsapp_number if c.isdigit())[2:]

    try:
        whatsapp_number = WhatsAppNumber.objects.get(number=cleaned_number)
        associated_companies = whatsapp_number.companies.all()

        # Check if the user is associated with any companies
        if associated_companies.exists():
            if incoming_message.upper().startswith("CL:"):
                company_id = incoming_message[3:]
                for company in associated_companies:
                    if str(company.id) == company_id:
                        company_name = company.name
                        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        message = client.messages.create(
                            content_sid='HX620c761514a511da496350731308ee0f',  # Your content template SID
                            from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',  # Your Twilio WhatsApp number or sender ID
                            content_variables=json.dumps({
                                '1': f"{company_name}",
                                '2': f"RE:{company_id}",
                                '3': f"QR:{company_id}",
                                '4': f"PR:{company_id}",

                            }),
                            to=sender_whatsapp_number,  # Recipient's WhatsApp number
                        )

                        return HttpResponse(message.sid)
            elif incoming_message.upper().startswith("RE:"):
                company_id = incoming_message[3:]
                for company in associated_companies:
                    if str(company.id) == company_id:
                        company_name = company.name
                        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        message = client.messages.create(
                            content_sid='HX2b3161b5afd09f10d2b0d81410bf80e6',  # Your content template SID
                            from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',  # Your Twilio WhatsApp number or sender ID
                            content_variables=json.dumps({
                                '1': f"{company_name}",
                                '2': f"DP:{company_id}/EPF",
                                '3': f"DP:{company_id}/ESI",
                                '4': f"Dp:{company_id}/GST",
                                '5': f"Dp:{company_id}/ITX",
                                '6': f"dP:{company_id}/ABK",
                                '7': f"dP:{company_id}/OTH",
                                '8': f"dp:{company_id}/DOC",

                            }),
                            to=sender_whatsapp_number,  # Recipient's WhatsApp number
                        )

                        return HttpResponse(message.sid)

            elif incoming_message.upper().startswith("DP:"):
                # Split the incoming message by '/'
                split_parts = incoming_message.split('/')

                # Extract company ID from the first part after splitting by ':'
                company_id = split_parts[0].split(':')[1]

                # Department is the second part after splitting by '/'
                department = split_parts[-1]

                for company in associated_companies:
                    if str(company.id) == company_id:
                        company_name = company.name
                        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        message = client.messages.create(
                            content_sid='HX5e551d67937697644f9ac349bf4a92dd',  # Your content template SID
                            from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',  # Your Twilio WhatsApp number or sender ID
                            content_variables=json.dumps({
                                '1': f"{company_name}",
                                '2': f"YR:{company_id}/{department}/",

                            }),
                            to=sender_whatsapp_number,  # Recipient's WhatsApp number
                        )

                        return HttpResponse(message.sid)
            elif incoming_message.upper().startswith("YR:"):
                # Split the incoming message by '/'
                split_parts = incoming_message.split('/')

                # Extract company ID from the first part after splitting by ':'
                company_id = split_parts[0].split(':')[1]

                # Department is the second part after splitting by '/'
                department = split_parts[1]
                year= split_parts[2]

                for company in associated_companies:
                    if str(company.id) == company_id:
                        company_name = company.name
                        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        message = client.messages.create(
                            content_sid='HX98b998878d0db9f38f1f4097863d1ddb',  # Your content template SID
                            from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',  # Your Twilio WhatsApp number or sender ID
                            content_variables=json.dumps({
                                '1': f"{company_name}",
                                '2': f"MTH:{company_id}/{department}/{year}/",
                                '3': f"MTH:{company_id}/{department}/{year}/",
                                '4': f"MTH:{company_id}/{department}/{year}/",
                                '5': f"MTH:{company_id}/{department}/{year}/",
                                '6': f"MTH:{company_id}/{department}/{year}/",
                                '7': f"MTH:{company_id}/{department}/{year}/",
                                '8': f"MTH:{company_id}/{department}/{year}/",
                                '9': f"MTH:{company_id}/{department}/{year}/",
                                '10': f"MTH:{company_id}/{department}/{year}/",
                                '11': f"MORE:{company_id}/{department}/{year}",

                            }),
                            to=sender_whatsapp_number,  # Recipient's WhatsApp number
                        )

                        return HttpResponse(message.sid)

            elif incoming_message.upper().startswith("MORE:"):
                # Split the incoming message by '/'
                split_parts = incoming_message.split('/')

                # Extract company ID from the first part after splitting by ':'
                company_id = split_parts[0].split(':')[1]

                # Department is the second part after splitting by '/'
                department = split_parts[1]
                year= split_parts[2]

                for company in associated_companies:
                    if str(company.id) == company_id:
                        company_name = company.name
                        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        message = client.messages.create(
                            content_sid='HX7ede93391e0f8fb47de6f130e89edbb3',  # Your content template SID
                            from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',  # Your Twilio WhatsApp number or sender ID
                            content_variables=json.dumps({
                                '1': f"{company_name}",
                                '2': f"MTH:{company_id}/{department}/{year}/",
                                '3': f"MTH:{company_id}/{department}/{year}/",
                                '4': f"MTH:{company_id}/{department}/{year}/",


                            }),
                            to=sender_whatsapp_number,  # Recipient's WhatsApp number
                        )

                        return HttpResponse(message.sid)
            elif incoming_message.upper().startswith("MTH:"):
                # Split the incoming message by '/'
                split_parts = incoming_message.split('/')

                # Extract company ID from the first part after splitting by ':'
                company_id = split_parts[0].split(':')[1]

                # Department is the second part after splitting by '/'
                department = split_parts[1]
                year= split_parts[2]
                month= split_parts[3]
                
                # Construct the base path based on the message components
                base_path = "/home/edwincamirtharaj/sfcy/media/uploads/{}/{}/{}/{}".format(company_id, department, year, month)

                for company in associated_companies:
                    if str(company.id) == company_id:
                        company_name = company.name
                        if os.path.exists(base_path):
                            # Iterate over all files in the directory structure
                            for root, _, files in os.walk(base_path):
                                # Iterate over each file
                                for file_name in files:
                                    # Construct the full file path
                                    file_path = os.path.join(root, file_name)
                                    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                                    message = client.messages.create(
                                                media_url=[file_path],  # Specify the URL of the file to be sent
                                                from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',
                                                to=sender_whatsapp_number,
                                    )

                            return HttpResponse(message.sid)
                        else:
                            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                            message = client.messages.create(
                                content_sid='HX4a59106df48819987f3a3e0e53934085',  # Your content template SID
                                from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',  # Your Twilio WhatsApp number or sender ID
                                to=sender_whatsapp_number,  # Recipient's WhatsApp number
                            )

                            return HttpResponse(message.sid)

            else:

                # Initialize variables for the first three companies
                first_company = 'Not Available'
                first_company_id = '0'
                second_company = incoming_message
                second_company_id = '0'
                third_company = 'Not Available'
                third_company_id = '0'

                # Iterate over the first three companies
                for index, company in enumerate(associated_companies):
                    if index == 0:
                        first_company = company.name
                        first_company_id = company.id
                    elif index == 1:
                        second_company = company.name
                        second_company_id = company.id
                    elif index == 2:
                        third_company = company.name
                        third_company_id = company.id
                    else:
                        break  # Stop looping after the third company

                # Construct the message
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    content_sid='HX6886a593a8edd2b9ceb18b78cbe15163',  # Your content template SID
                    from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',  # Your Twilio WhatsApp number or sender ID
                    content_variables=json.dumps({
                        '1': f"{first_company}",
                        '2': f"CL:{first_company_id}",
                        '3': f"{second_company}",
                        '4': f"CL:{second_company_id}",
                        '5': f"{third_company}",
                        '6': f"Cl:{third_company_id}",

                    }),
                    to=sender_whatsapp_number,  # Recipient's WhatsApp number
                )

                return HttpResponse(message.sid)

        else:
            # If the user is not associated with any companies, handle accordingly
            response = MessagingResponse()
            response.message("You are not associated with any companies.")
            return HttpResponse(str(response))

    except WhatsAppNumber.DoesNotExist:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            content_sid='HXd2501d4d90ac26fb9c3c353c97589c55',  # Your content template SID
            from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',  # Your Twilio WhatsApp number or sender ID
            to=sender_whatsapp_number,  # Recipient's WhatsApp number
        )

        return HttpResponse(message.sid)




@csrf_exempt
def handle_whatsapp_message_old(request: HttpRequest):
    # Extract data from Twilio request
    incoming_message = request.POST.get('Body', '')
    sender_whatsapp_number = request.POST.get('From', '')

    cleaned_number = ''.join(c for c in sender_whatsapp_number if c.isdigit())[2:]

    try:
        whatsapp_number = WhatsAppNumber.objects.get(number=cleaned_number)
        associated_companies = whatsapp_number.companies.all()

        # Check if the user is associated with any companies
        if associated_companies.exists():
    # Initialize variables for the first three companies
            first_company = 'Not Available'
            first_company_id = '0'
            second_company = incoming_message
            second_company_id = '0'
            third_company = 'Not Available'
            third_company_id = '0'

    # Iterate over the first three companies
            for index, company in enumerate(associated_companies):
                if index == 0:
                    first_company = company.name
                    first_company_id = company.id
                elif index == 1:
                    second_company = company.name
                    second_company_id = company.id
                elif index == 2:
                    third_company = company.name
                    third_company_id = company.id
                else:
                    break  # Stop looping after the third company

    # Construct the message
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                content_sid='HX6886a593a8edd2b9ceb18b78cbe15163',  # Your content template SID
                from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',  # Your Twilio WhatsApp number or sender ID
                content_variables=json.dumps({
                    '1': f"{first_company}",
                    '2': f"CL:{first_company_id}",
                    '3': f"{second_company}",
                    '4': f"CL:{second_company_id}",
                    '5': f"{third_company}",
                    '6': f"Cl:{third_company_id}",

                }),
                to=sender_whatsapp_number,  # Recipient's WhatsApp number

            )

            return HttpResponse(message.sid)

        else:
            # If the user is not associated with any companies, handle accordingly
            response = MessagingResponse()
            response.message("You are not associated with any companies.")
            return HttpResponse(str(response))

    except WhatsAppNumber.DoesNotExist:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            content_sid='HXd2501d4d90ac26fb9c3c353c97589c55',  # Your content template SID
            from_='MGe231d2e95e5b34cffc0c2472bc7bf02e',  # Your Twilio WhatsApp number or sender ID
            to=sender_whatsapp_number,  # Recipient's WhatsApp number
        )


        return HttpResponse(message.sid)



