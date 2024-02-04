from django.test import TestCase
from twilio.rest import Client

account_sid = 'ACc0cb016b1cdbf70a5d5d013caf421cd5'
auth_token = '2ec96105b79b0c9d7ef00e23711a498c'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Send by SFCY',
  to='whatsapp:+919489334112'
)

print(message.sid)
# Create your tests here.
