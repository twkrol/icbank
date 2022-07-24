from django.db import transaction

from .models import Account, Transfer


def transfer_and_update(number_debited, number_credited, amount):
    if src := Account.objects.filter(number=number_debited).first():
        if amount > src.balance:
            raise Exception("Insufficient funds")

        if amount <= 0:
            raise Exception("Amount to transfer must be greater than 0")

        if dst := Account.objects.filter(number=number_credited).first():
            if src.number == dst.number:
                raise Exception("Transfer accounts must be different")
            with transaction.atomic():
                transfer = Transfer(number_debited=src.number, number_credited=dst.number, amount=amount)
                transfer.save()
                src.balance -= amount
                src.save()
                dst.balance += amount
                dst.save()
        else:
            raise Exception("Unknown account number to credit")
    else:
        raise Exception("Unknown account number to debit")