from django.urls import path

from . import views

urlpatterns = [
    path('', views.webhook_messenger, name="bot-webhook"),
]
