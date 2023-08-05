from django.urls import path
from .views import facebook_webhook, home

urlpatterns = [
    path('', home, name='home'),
    path('webhook/', facebook_webhook, name='facebook_webhook'),
]
