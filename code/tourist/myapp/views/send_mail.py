
from django.core.mail import send_mail
def send_mail_function(email_title, email, email_body):
    try:
        finish_send = send_mail(
            email_title,
            None,
            "tripfunchill@gmail.com",
            [email],
            html_message=email_body,
        )
        if finish_send:
            print(f"Email sent successfully to {email}")
        else:
            print(f"Email sending failed to {email}")
        return finish_send
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
