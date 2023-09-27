from django.shortcuts import render

from config.settings import EMAIL_HOST_USER, SITE_NAME

def confirmation_view(request):
    return render(request,'account/confirmation.html')

# views.py

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet
from django.db import IntegrityError
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from core.tokens import account_activation_token, send_activation_email

class CustomUserViewSet(UserViewSet):
    def create(self, request, *args, **kwargs):
        try:
            # Extract user data from the request
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')

            # Ensure that email, username, and password are provided
            if not (username and email and password):
                return Response(
                    {"success": False, "error_message": "Email, username, and password are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create a new user using get_user_model() and set is_active to False
            User = get_user_model()
            custom_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False,
            )

            custom_user = User.objects.get(username=username)
            # Generate the activation URL
            uid = urlsafe_base64_encode(force_bytes(custom_user.pk))
            token = default_token_generator.make_token(custom_user)
            protocol = 'https' if request.is_secure() else 'http'  # Detect the protocol
            domain = get_current_site(request).domain  # Get the domain
            activation_url = f"activate/{uid}/{token}"

            # Context data to pass to the email template
            context = {
                'site_name': get_current_site(request).name,
                'protocol': protocol,
                'domain': domain,
                'url': activation_url,
            }

            # Render the email content using the template
            # email_subject = render_to_string('activation_email_subject.txt', context)
            email_body = render_to_string('account/activation.html', context)
            recipient_email = custom_user.email
            email_message=EmailMultiAlternatives(SITE_NAME,'',EMAIL_HOST_USER,[recipient_email],)
            email_message.attach_alternative(email_body , 'text/html')

# Send the email
            email_message.send()
            # send_mail(
            #     SITE_NAME,
            #     email_body,
            #     EMAIL_HOST_USER,
            #     [recipient_email],
            #     fail_silently=False,
            # )
            # --------------------------------------------
                # Generate an activation token for the user
            # uid = urlsafe_base64_encode(force_bytes(custom_user.pk))
            # token = account_activation_token.make_token(custom_user)

            # # Create an activation link
            # activation_link = request.build_absolute_uri(reverse('activation', kwargs={'uid': uid, 'token': token}))

            # # Send the activation email
            # send_activation_email(request, custom_user.email, activation_link, uid, token)

            # Customize the response data for successful creation
            response_data = {
                "success": True,
                "username": custom_user.username,
                "email": custom_user.email,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            # Handle database integrity errors (e.g., duplicate email or username)
            response_data = {
                "success": False,
                "error_message": "User with this email or username already exists.",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle other exceptions
            response_data = {
                "success": False,
                "error_message": str(e),
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
