from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *


class PANAdmin(ModelAdmin):
    list_display = ['user', 'pan_number']


class WalletAdmin(ModelAdmin):
    list_display = ['user', 'amount']


admin.site.register(PAN_Verification, PANAdmin)
admin.site.register(Wallet, WalletAdmin)