from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
import time

@shared_task(serializer='json', name="send_mail")
def send_email_fun(subject, message, sender, receiver):
    time.sleep(5) # for check that sending email process runs in background 
    # send_mail(subject, message, sender, [receiver])
    subject = "Task Completion Notification"
    html_message = render_to_string('mail.html')

    send_mail(
        subject,
        "",
        sender, 
        [receiver],
        fail_silently=False,
        html_message=html_message,
    )