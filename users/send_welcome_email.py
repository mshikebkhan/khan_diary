from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail, EmailMultiAlternatives


def send_welcome_email(first_name, email):
    """ Send welcome mail to the new users. """

    # Prepare mail
    mail_text = get_template('users/welcome_email.html')
    mail_context = { 'first_name': first_name, 'domain': settings.DEFAULT_DOMAIN }
    mail_content = mail_text.render(mail_context)

    # Send email to the newly registered user.
    mail = EmailMultiAlternatives("Welcome to Khan Diary", mail_content, settings.DEFAULT_FROM_EMAIL, [email])
    mail.content_subtype = 'html'
    mail.send(fail_silently=True) 
    
