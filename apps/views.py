from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.http import Http404
from django.db import transaction

from users.models import CustomUser
from .models import Transaction
from .serializers import TransactionSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache


class ListTransaction(APIView):
    permission_classes = [IsAuthenticated]
    
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*60))
    def get(self, request, format=None):
        user = request.user
        data = Transaction.objects.filter(account = user)
        print('DATA :', data)
        serializer = TransactionSerializer(data, many=True)
        content = {
            'user':user.email,
            'status': 'request was permitted',
            'Data':serializer.data
        }
        return Response(content)
    
    def post(self, request, format=None):
        print('Cache : ',cache.clear())
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            with transaction.atomic():
                usr = CustomUser.objects.select_for_update().get(email=request.user)
                if request.data.get('transaction_type') == '1':
                    
                    usr.balance += int(request.data.get('amount'))
                    serializer.save(account = request.user, balance_after_transaction = float(usr.balance))
                    usr.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                
                if request.data.get('transaction_type') == '2':
                    if int(request.data.get('amount')) < int(usr.balance):
                        usr.balance -= int(request.data.get('amount'))
                        serializer.save(account = request.user, balance_after_transaction = float(usr.balance))
                        usr.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.data, status=status.HTTP_400)
    