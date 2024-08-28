from datetime import datetime, timedelta
from smtplib import SMTPException

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from message.models import MailingList, Attempt


def sending_a_message(item: MailingList):
    """
    Отправка сообщения клиенту с использованием SMTP
    """
    try:
        send_mail(
            item.message.title_letter,
            item.message.body_letter,
            EMAIL_HOST_USER,
            [x.email for x in item.clients.all()],
            fail_silently=False,
        )
    except SMTPException as message:
        Attempt.objects.create(
            mailing_list=item,
            mail_server_response=f"{message}"
        )
    else:
        Attempt.objects.create(
            mailing_list=item,
            status='Успешно',
            mail_server_response="Доставлено"
        )


def periodicity_sending():
    """
    Отправка сообщения клиенту каждый день
    """
    mailing_list = MailingList.objects.filter(next_date__lte=datetime.now())
    for mailing in mailing_list:
        if mailing.status == 'Запущена':
            sending_a_message(mailing)
            if mailing.periodicity == 'Раз в день':
                mailing.next_date = mailing.next_date + timedelta(days=1)
            if mailing.periodicity == 'Раз в неделю':
                mailing.next_date = mailing.next_date + timedelta(days=7)
            if mailing.periodicity == 'Раз в месяц':
                mailing.next_date = mailing.next_date + timedelta(days=30)
            mailing.save(update_fields=['next_date'])





