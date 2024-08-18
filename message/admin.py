from django.contrib import admin

from message.models import Message, Client, MailingList, Attempt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Админка модели Message
    """
    list_display = ('id', 'title_letter')
    search_fields = ('title_letter',)


@admin.register(Client)
class ClientsAdmin(admin.ModelAdmin):
    """
    Админка модели Clients
    """
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    """
    Админка модели MailingList
    """
    list_display = ('id', 'message', 'periodicity', 'status')
    list_filter = ('periodicity', 'status')
    search_fields = ('message',)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    """
    Админка модели Attempt
    """
    list_display = ('mailing_list', 'status', 'mail_server_response')
    list_filter = ('status',)
    search_fields = ('mailing_list', 'mail_server_response')

