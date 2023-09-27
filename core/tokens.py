from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.contrib.sites.shortcuts import get_current_site


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()

import uuid

def generate_activation_token():
    return str(uuid.uuid4())

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.conf import settings


def send_activation_email(request, email, activation_link, uid, token):
    pass
    # subject = 'Activate your account'
    
    # # Get the HTML template
    # html_template = get_template('account/activation.html')
    
    # # Render the template with the context data
    # context = {'activation_link': activation_link}
    
    # message = html_template.render(context)
    
    # from_email = settings.EMAIL_HOST_USER
    # recipient_list = [email]
    
    # # Create an EmailMessage with HTML content
    # email = EmailMessage(subject, message, from_email, recipient_list)
    # email.content_subtype = 'html'  # Set the content type to HTML
    # email.send()
