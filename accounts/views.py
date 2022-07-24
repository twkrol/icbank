from email.policy import default
from urllib import response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import APIException
from rest_framework.parsers import JSONParser
from django.db.models import Q

from .models import Account, Transfer
from .serializers import AccountInfoSerializer, AccountCreateSerializer, TransferSerializer, TransferCreateSerializer
from .services import transfer_and_update


@api_view(['POST'])
def create(request):
    '''Metoda generuje nowy rachunek dla podanego właściciela, np.:
        {"owner": "John Kowalsky"}
    '''
    serializer = AccountCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def balance(request):
    '''Metoda zwraca informację o stanie rachunku, np.:
        {"number": "PL81100010014322624589612440"}
    '''
    serializer = AccountInfoSerializer(data=request.data)
    if serializer.is_valid():
        if account := Account.objects.filter(number=serializer.validated_data.get('number')).first():        
            return Response(account.balance)
        else:
            content = {"detail": "Unknown account number"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def transfer(request):
    '''Metoda przesyła środki pomiędzy rachunkami, np.:
        {
            "number_debited": "PL81100010014322624589612440",
            "number_credited": "PL54100010016371142857958553",
            "amount": "50"
        }
    '''
    serializer = TransferCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            transfer_and_update(
                number_debited=serializer.validated_data.get('number_debited'),
                number_credited=serializer.validated_data.get('number_credited'),
                amount=serializer.validated_data.get('amount'),
            )
            return Response('Transfer executed')
        except Exception as e:
            content = {"detail": str(e)}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@parser_classes([JSONParser])
def history(request):
    '''Metoda zwraca informację o historii rachunku, np.:
        {"number": "PL81100010014322624589612440"}
    '''
    serializer = AccountInfoSerializer(data=request.data)
    if serializer.is_valid():
        number = serializer.validated_data.get('number')
        history = Transfer.objects.filter(Q(number_debited=number) | Q(number_credited=number))
        result = TransferSerializer(history, many=True)
        return Response(result.data)
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
