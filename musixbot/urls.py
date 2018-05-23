from django.urls import path, include

urlpatterns = [
    path('webhook/', include('bot.urls')),
]
