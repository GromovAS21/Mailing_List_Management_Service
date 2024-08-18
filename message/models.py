from django.db import models


class Message(models.Model):
    """
    Модель сообщения для рассылки писем
    """
    title_letter = models.CharField(
        max_length=100,
        verbose_name="Тема письма",
    )
    body_letter = models.TextField(
        verbose_name="Содержание письма",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.title_letter


class Clients(models.Model):
    """
    Модель клиента для рассылки писем (кому отправляется письмо)
    """
    name = models.CharField(
        max_length=250,
        verbose_name="Ф.И.О",
        help_text="Введите Ф.И.О. получателя"
    )
    email = models.EmailField(
        verbose_name="Email",
        unique=True
    )

    comment = models.TextField(
        max_length=100,
        verbose_name="Комментарий",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f'{self.name} ({self.email})'


class MailingList(models.Model):
    """
    Параметры рассылки
    """
    PERIODICITY_CHOICES = [
        ('DAILY', 'Раз в день'),
        ('WEEKLY', 'Раз в неделю'),
        ('MONTHLY', 'Раз в месяц')
    ]
    STATUS_CHOICES = [
        ('COMPLETED', 'Завершена'),
        ('CREATED', 'Создана'),
        ('RUNNING', 'Запущена')
    ]
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="messages"
    )
    clients = models.ManyToManyField(
        Clients,
        verbose_name="Клиенты"
    )
    periodicity = models.CharField(
        max_length=50,
        choices=PERIODICITY_CHOICES,
        verbose_name="Периодичность рассылки",
        default="DAILY"
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="CREATED",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Рассылка N {self.pk}"


class Attempt(models.Model):
    """
    Попытка отправки рассылки
    """
    STATUS_CHOICES = [
        ('SUCCESS', 'Успешно'),
        ('FAILURE', 'Не успешно'),
    ]
    mailing_list = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="attempts"
    )
    date_time_last_attempt = models.DateTimeField(
        verbose_name="Дата и время последнего попытки отправки",
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        verbose_name="Статус попытки",
        default='FAILURE'
    )
    mail_server_response = models.TextField(
        verbose_name="Ответ почтового сервера"
    )

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"

    def __str__(self):
        return f"Попытка отправки письма N {self.pk}"
