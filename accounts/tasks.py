from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime as dt

from django.contrib.auth.models import User


#sends information email to admin every week that contains criticalProducts etc.
def sendInformationEmail():

    #get all users who are Staff
    users = User.objects.filter(groups__name='admin')

    date = timezone.now()
    date = dt.strftime(date, '%Y-%m-%d')
    date = str(date)

    #URL of the report download page
    #may make it dynamic in the future
    report = "https://managemt.herokuapp.com/pdf_view/" + date

    #send email to each staff
    for user in users:
        template = render_to_string('accounts/email_template.html', {'name': user.username, 'report': report})
        email = EmailMessage(
            'Depo Takip Sistemi - Haftalık Rapor',
            template,
            settings.EMAIL_HOST_USER,
            [ user.email, ],
        )
        print("Sending email to: " + user.email)

        email.fail_silently = False
        email.send()
