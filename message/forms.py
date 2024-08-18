from django.forms import ModelForm, BooleanField

from message.models import Message

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
