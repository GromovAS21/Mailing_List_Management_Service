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
            mail_server_response=message
        )
    else:
        Attempt.objects.create(
            mailing_list=item,
            status='Успешно',
            mail_server_response="Доставлено"
        )

