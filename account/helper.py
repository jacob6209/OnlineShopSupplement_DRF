from django.conf import settings
from twilio.rest import Client 
from rest_framework.response import Response
from rest_framework import status
import random

class MessageHandler:

    phone_number=None
    opt=None
    otp = str(random.randint(100000, 999999))
    
    def __init__(self,phone_Number) -> None:
        self.phone_number=phone_Number

    def send_otp_on_phone(self):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'Your OTP is: {self.otp}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=self.phone_number
        )
        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)