from django.urls import path
from .views import ListTransaction

urlpatterns = [
    path('transaction/', ListTransaction.as_view(), name='List Transaction')
]
