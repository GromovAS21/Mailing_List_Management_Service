from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from message.forms import MessageForm, ClientForm, MailingListForm, MailingUpdateForm
from message.models import Message, Client, MailingList


class MessageListView(ListView):
    """
    Контроллер для отображения всех сообщений
    """
    model = Message

    def get_queryset(self):
        """
        Возвращает сообщения текущего пользователя
        """
        if self.request.user.is_superuser:
            return Message.objects.all()
        elif self.request.user.is_authenticated:
            return Message.objects.filter(owner=self.request.user)
        else:
            return Message.objects.none()


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для отображения конкретного сообщения
    """
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания нового сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_view')

    def form_valid(self, form):
        """
        Сохраняет сообщение в БД и привязывает его к текущему пользователю

        """
        message = form.save()
        message.owner = self.request.user
        message.save(update_fields=['owner'])
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для редактирования сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_view')

    def get_success_url(self):
        return reverse('message:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер для удаления сообщения
    """
    model = Message
    success_url = reverse_lazy('message:message_view')


class ClientListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения всех клиентов
    """
    model = Client

    def get_queryset(self):
        """
        Возвращает клиентов текущего пользователя
        """
        if self.request.user.is_superuser:
            return Client.objects.all()
        if self.request.user.is_authenticated:
            return Client.objects.filter(owner=self.request.user)
        else:
            return None


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для отображения конкретного клиента
    """
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания нового клиента
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('message:client_view')

    def form_valid(self, form):
        """
        Сохраняет клиента в БД и привязывает его к текущему пользователю

        """
        client = form.save()
        client.owner = self.request.user
        client.save(update_fields=['owner'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('message:client_detail', kwargs={'pk': self.object.pk})



class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для редактирования клиента
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('message:client_view')

    def get_success_url(self):
        return reverse('message:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер для удаления клиента
    """
    model = Client
    success_url = reverse_lazy('message:client_view')


class MailingListListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения всех рассылок
    """
    model = MailingList

    def get_queryset(self):
        """
        Возвращает рассылки текущего пользователя
        """
        return MailingList.objects.filter(owner=self.request.user)


class MailingListCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания новой рассылки
    """
    model = MailingList
    form_class = MailingListForm

    def form_valid(self, form):
        """
        Обновляет дату следующей отправки при сохранении изменений
        """
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.next_date = mailing.date_and_time_of_sending
        mailing.save(update_fields=['next_date', 'owner'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('message:mailinglist_detail', kwargs={'pk': self.object.pk})




class MailingListDetailView(LoginRequiredMixin, DetailView):
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


class MailingListUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для создания новой рассылки
    """
    model = MailingList
    form_class = MailingUpdateForm

    def form_valid(self, form):
        """
        Обновляет дату следующей отправки и статус рассылки при сохранении изменений
        """
        mailing = form.save()
        mailing.next_date = mailing.date_and_time_of_sending
        mailing.status = "Запущена"
        mailing.save(update_fields=['next_date', 'status'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('message:mailinglist_detail', kwargs={'pk': self.object.pk})


class MailingListDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер для удаления рассылки
    """
    model = MailingList
    success_url = reverse_lazy('message:mailinglist_view')


@login_required
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


@login_required
def AttemptListView(request, pk):
    """
    Контроллер для отображения всех попыток отправки рассылки
    """
    mailing = get_object_or_404(MailingList, pk=pk)
    attempts = mailing.attempts.all()
    numbers = [number for number in range(1,len(attempts) + 1)]
    context = {
        'attempts': attempts,
        'mailing': mailing,
        'numbers': numbers
    }
    return render(request,'message/attempt_list.html', context)
