from django.urls import path
from faucet.views import TransactionApi

urlpatterns = [path("airdrops/", TransactionApi.as_view())]
