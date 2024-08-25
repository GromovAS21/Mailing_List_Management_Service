from django.forms import ModelForm, BooleanField, TextInput

from message.models import Message, Client, MailingList


class StyleFormMixin:
    """
    Mixin для стилизации формы.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class MessageForm(StyleFormMixin, ModelForm):
    """
    Форма для создания нового сообщения
    """
    class Meta:
        model = Message
        fields = ('title_letter', 'body_letter')
        widgets = {
            'title_letter': TextInput(attrs={'placeholder': 'Введите тему сообщения'}),
        }


class ClientForm(StyleFormMixin, ModelForm):
    """
    Форма для создания нового клиента
    """
    class Meta:
        model = Client
        fields = ('name', 'email', 'comment')
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Введите Ф.И.О.'}),
            'email': TextInput(attrs={'placeholder': 'Введите Email'}),
            'comment': TextInput(attrs={'placeholder': 'Введите текст'}),
        }


class MailingListForm(StyleFormMixin, ModelForm):
    """
    Форма для создания рассылки сообщения
    """
    class Meta:
        model = MailingList
        fields = ('message', 'clients', 'periodicity',)
