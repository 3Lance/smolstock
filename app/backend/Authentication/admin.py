from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import ModelAdmin


class UserAdmin(BaseUserAdmin):
    ordering = ['id', 'name']
    list_display = ['id', 'name', 'email']
    list_filter = ('is_superuser',)
    filter_horizontal = ()
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name','profile_picture')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff',)}),
    )
    add_fieldsets = (
        ('User Credentials', {'fields': ('email', 'password1', 'password2')}),
        ('Personal Info', {'fields': ( 'name','profile_picture')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff',)}),
    )


class TFVAdmin(ModelAdmin):
    list_display = ['user', 'phone_number']


class TFOAdmin(ModelAdmin):
    list_display = ['phone_number', 'otp', 'created_time']


class EOAdmin(ModelAdmin):
    list_display = ['user', 'otp', 'created_time']


class SUUAdmin(ModelAdmin):
    list_display = ['email', 'token_generated_at', 'is_verified']


admin.site.register(User, UserAdmin)
admin.site.register(Two_Factor_Verification, TFVAdmin)
admin.site.register(Two_Factor_OTP, TFOAdmin)
admin.site.register(Email_OTP, EOAdmin)
admin.site.register(SignUpUser, SUUAdmin)
