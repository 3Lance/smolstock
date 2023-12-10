from django.db.models.base import Model
from django.db.models.fields import FloatField, CharField
from django.db.models.fields.related import OneToOneField
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from Investments.models import MyHoldings, TransactionHistory
import string
import random
from Authentication.models import User


class PAN_Verification(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='pan_details')
    pan_number = CharField(unique=True, max_length=10,
                           validators=[RegexValidator(regex='[A-Z]{5}[0-9]{4}[A-Z]{1}', message='Invalid PAN',),])

@receiver(post_save, sender=PAN_Verification)
def create_referal_code(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user = instance.user)
        MyHoldings.objects.create(user =instance. user,  MyHoldings = [])
        TransactionHistory.objects.create(user = instance.user, transactions = [])


class Wallet(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='wallet')
    amount = FloatField(default=10000)
    referal = CharField(max_length=6, null=True, blank=True)

@receiver(post_save, sender=Wallet)
def make_referal_code(sender, instance, created, **kwargs):
    if created:
        id = str(instance.user.id)
        instance.referal = ''.join(random.choices(string.ascii_uppercase, k = 6 - len(id))) + id
        instance.save()