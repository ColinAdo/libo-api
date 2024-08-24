from django.conf import settings
from django.core.mail import send_mail

from .models import Progress


from celery import shared_task

# Signal to update progresses and send mails after the book is completed
@shared_task
def send_completion_email_after_seven_days(progress_id):
    progress = Progress.objects.get(id=progress_id)
    if progress.remaining_time == 0:
        progress.mark_as_complete()
        progress.is_reading = False
        progress.save()

        domain = f'http://localhost:8000/{progress.book.pdf_file.url}'
        subject = f'{progress.book.title} completion'
        message = f'Hey {progress.user.username}, \n\n \
                You have completed reading {progress.book.title} book. \n\n \
                You can download it from here {domain}. \n\n \
                Never stop learning, remember readers are leaders! \n\n \
                The Libo http://localhost:8000 team.'

        send_mail(
            subject,  
            message, 
            settings.AWS_SES_FROM_EMAIL, 
            [f'{progress.user.email}'], 
        )
       
        