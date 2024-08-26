from smtplib import SMTPException

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from message.models import MailingList, Attempt


def sending_a_message(item: MailingList, client):
    """
    Отправка сообщения клиенту с использованием SMTP
    """
    try:
        send_mail(
            item.message.title_letter,
            item.message.body_letter,
            EMAIL_HOST_USER,
            [client.email],
            fail_silently=False,
        )
    except SMTPException as message:
        Attempt.objects.create(
            mailing_list=item,
            mail_server_response=f"{client.email} - {message}"
        )
    else:
        Attempt.objects.create(
            mailing_list=item,
            status='Успешно',
            mail_server_response=f"{client.email} - Доставлено"
        )


def sending_mail_every_day(item: MailingList, client):
    """
    Отправка сообщения клиенту каждый день
    """
    sending_a_message(item, client)


def sending_mail_every_week(item: MailingList, client):
    """
    Отправка сообщения клиенту каждую неделю
    """
    sending_a_message(item, client)


def sending_mail_every_month(item: MailingList, client):
    """
    Отправка сообщения клиенту каждый месяц
    """
    sending_a_message(item, client)

