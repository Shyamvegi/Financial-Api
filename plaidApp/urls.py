from django.urls import path, include
from .views import GetAccessToken, GetTransactions,Webhook,GetLinkToken,PlaidConnect

urlpatterns = [
    path('', PlaidConnect),
    path('get-access-token/', GetAccessToken.as_view()),
    path('get-transactions/', GetTransactions.as_view()),
    path('get-link-token/', GetLinkToken.as_view()),
    path('webhook/', Webhook.as_view()),
]