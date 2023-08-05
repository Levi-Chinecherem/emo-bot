from django.urls import path
from .views import facebook_webhook, home, documentation

urlpatterns = [
    path('', home, name='home'),
    path('documentation/', documentation, name='documentation'),
    path('webhook/', facebook_webhook, name='facebook_webhook'),
]
