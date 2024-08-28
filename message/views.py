from datetime import datetime

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from message.forms import MessageForm, ClientForm, MailingListForm
from message.models import Message, Client, MailingList
from message.services import periodicity_sending


# Create your views here.
class MessageListView(ListView):
    """
    Контроллер для отображения всех сообщений
    """
    model = Message


class MessageDetailView(DetailView):
    """
    Контроллер для отображения конкретного сообщения
    """
    model = Message


class MessageCreateView(CreateView):
    """
    Контроллер для создания нового сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_view')


class MessageUpdateView(UpdateView):
    """
    Контроллер для редактирования сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_view')

    def get_success_url(self):
        return reverse('message:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(DeleteView):
    """
    Контроллер для удаления сообщения
    """
    model = Message
    success_url = reverse_lazy('message:message_view')


class ClientListView(ListView):
    """
    Контроллер для отображения всех клиентов
    """
    model = Client


class ClientDetailView(DetailView):
    """
    Контроллер для отображения конкретного клиента
    """
    model = Client


class ClientCreateView(CreateView):
    """
    Контроллер для создания нового клиента
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('message:client_view')

    def get_success_url(self):
        return reverse('message:client_detail', kwargs={'pk': self.object.pk})


class ClientUpdateView(UpdateView):
    """
    Контроллер для редактирования клиента
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('message:client_view')

    def get_success_url(self):
        return reverse('message:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(DeleteView):
    """
    Контроллер для удаления клиента
    """
    model = Client
    success_url = reverse_lazy('message:client_view')


class MailingListListView(ListView):
    """
    Контроллер для отображения всех рассылок
    """
    model = MailingList


class MailingListCreateView(CreateView):
    """
    Контроллер для создания новой рассылки
    """
    model = MailingList
    form_class = MailingListForm

    def form_valid(self, form):
        mailing = form.save()
        mailing.next_date = mailing.date_and_time_of_sending
        mailing.save(update_fields=['next_date'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('message:mailinglist_detail', kwargs={'pk': self.object.pk})


class MailingListDetailView(DetailView):
    """
    Контроллер для отображения конкретной рассылки
    """
    model = MailingList

    def get_context_data(self, **kwargs):
        """
        Добавляет список клиентов к контексту
        """
        context_data = super().get_context_data(**kwargs)
        context_data['clients'] = self.object.clients.all()
        return context_data


class MailingListUpdateView(UpdateView):
    """
    Контроллер для создания новой рассылки
    """
    model = MailingList
    form_class = MailingListForm

    def form_valid(self, form):
        mailing = form.save()
        mailing.next_date = mailing.date_and_time_of_sending
        mailing.status = "Запущена"
        mailing.save(update_fields=['next_date', 'status'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('message:mailinglist_detail', kwargs={'pk': self.object.pk})


class MailingListDeleteView(DeleteView):
    """
    Контроллер для удаления рассылки
    """
    model = MailingList
    success_url = reverse_lazy('message:mailinglist_view')


def toggle_status(request, pk):
    """
    Метод изменения статуса рассылки
    """
    mailing = get_object_or_404(MailingList, pk=pk)
    if mailing.status == 'Запущена':
        mailing.status = 'Завершена'
    elif mailing.status == 'Создана':
        mailing.status = 'Запущена'
    mailing.save(update_fields=['status',])
    return redirect(reverse('message:mailinglist_view'))
