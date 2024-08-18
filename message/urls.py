from django.urls import path

from message.apps import MessageConfig
from message.views import MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MessageConfig.name

urlpatterns = [
    path('', MessageListView.as_view(), name='message_view'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete-confirm', MessageDeleteView.as_view(), name='message_delete'),
]