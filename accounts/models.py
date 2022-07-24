import random
import string

from schwifty import IBAN
from django.db import models

BANK_COUNTRY_CODE = 'PL'
BANK_CODE = '10001001'
ACCOUNT_NUMBER_LENGTH = 16

def _make_account_number():
    new_number = ''.join(random.choice(string.digits) for i in range(ACCOUNT_NUMBER_LENGTH))
    iban = IBAN.generate(BANK_COUNTRY_CODE, bank_code=BANK_CODE, account_code=new_number)
    return iban


class Account(models.Model):
    number = models.CharField(max_length=28, default=_make_account_number)
    owner = models.CharField(max_length=255)
    balance = models.IntegerField(default=0)
    
    class Meta:
        indexes = [models.Index(fields=['number', ]), ]

    def __str__(self) -> str:
        iban = IBAN(self.number)
        return iban.formatted


class Transfer(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    number_debited = models.CharField(max_length=28)
    number_credited = models.CharField(max_length=28)
    amount = models.PositiveIntegerField()

    class Meta:
        ordering = ('timestamp',)
        indexes = [models.Index(fields=['timestamp', ]), ]
