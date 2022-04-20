from django.conf import settings
from django.core.mail import send_mail

def send_message(mail):
    subject = "Congratulation on winning bid!"
    message = f'Hi {mail}, you have won the bid in property you put your bid on. Try contacting agent for further information'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [mail, ]
    send_mail(subject,message,email_from,recipient_list)
    return