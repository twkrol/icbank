from rest_framework import serializers

from .models import Account, Transfer


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['owner', 'number', 'balance', ]
        read_only_fields = ['number', 'balance', ]


class AccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['number', 'balance', 'owner', ]
        read_only_fields = ['balance', 'owner', ]


class TransferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['number_debited', 'number_credited', 'amount', ]


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['timestamp', 'number_debited', 'number_credited', 'amount', ]
