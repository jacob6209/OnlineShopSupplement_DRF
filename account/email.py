from djoser import email

#this is email.py located in account app :

class ActivationEmail(email.ActivationEmail):
    template_name = 'account/activation.html'


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'account/confirmation.html'


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'account/password_reset.html'


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = 'account/password_changed_confirmation.html'
