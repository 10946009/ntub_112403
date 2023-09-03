from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_mail_function(email_title, email, email_body): 
    send_mail(
        email_title,
        None,
        "tripfunchill@gmail.com",
        [email],
        html_message=email_body,
    )

# @shared_task
# def send_mail_function(email_title, email, email_body):
#     send_mail(
#         email_title,
#         None,
#         "tripfunchill@gmail.com",
#         [email],
#         html_message=email_body,
#     )