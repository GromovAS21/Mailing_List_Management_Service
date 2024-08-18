from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from message.forms import MessageForm
from message.models import Message


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

    def get_success_url(self):
        return reverse('message:message_detail', kwargs={'pk': self.object.pk})


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






