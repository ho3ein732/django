from django.core.mail import send_mail
import random


def send_verification_code(email, verification_code):
    subject = 'کد تایید سایت من'
    message = f'{verification_code}کد تایید شما : '
    from_email = 'example@example.com'
    send_mail(subject, message,
              from_email, email)


def generate_random_code():
    return ''.join(random.choices('0123456789', k=6))
