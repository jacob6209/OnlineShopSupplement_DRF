# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# import six
# from django.contrib.sites.shortcuts import get_current_site


# class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#                 six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
#         )


# account_activation_token = AccountActivationTokenGenerator()

# import uuid

# def generate_activation_token():
#     return str(uuid.uuid4())




# def send_activation_email(request, email, activation_link, uid, token):
#     pass
