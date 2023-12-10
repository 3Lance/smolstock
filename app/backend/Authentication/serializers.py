from rest_framework.serializers import Serializer, EmailField, CharField, BooleanField, IntegerField, UUIDField
from django.contrib.auth import authenticate
from .models import User, Two_Factor_Verification
from .utils import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password


class LoginSerializer(Serializer):
    email = EmailField(write_only = True)
    password = CharField(write_only = True)
    two_factor = BooleanField(read_only = True)
    refresh = CharField(read_only = True)
    access = CharField(read_only = True)

    def validate(self,data):
        inemail = normalize_email(data['email'])
        if not User.objects.filter(email = inemail).exists():
            raise CustomError('User not registered')
        user = authenticate(email=inemail, password=data['password'])
        if not user:
            raise CustomError('Invalid Credentials')
        try:
            mobile = Two_Factor_Verification.objects.get(user = user)
            if not mobile.enabled:
                raise ObjectDoesNotExist
            data['two_factor'] = True
            if resend_otp(user, twofactor = True):
                send_two_factor_otp(mobile)
        except ObjectDoesNotExist:
            data['refresh'] = user.refresh
            data['access'] = user.access
            data['two_factor'] = False
        return data


class VerifyTwoFactorOTPSerializer(Serializer):
    email = EmailField(write_only = True)
    otp = IntegerField(write_only = True)
    refresh = CharField(read_only = True)
    access = CharField(read_only = True)

    def validate(self, data):
        user = User.objects.filter(email = normalize_email(data['email']))
        if not user.exists():
            raise CustomError('User not registered')
        user = user[0]
        response = validateOTP(user, data['otp'], twofactoron = True)
        if response == 'OK':
            data['refresh'] = user.refresh
            data['access'] = user.access
            return data
        raise CustomError(response)


class SendOTPEmailSerializer(Serializer):
    email = EmailField()

    def validate(self, data):
        user = User.objects.filter(email = normalize_email(data['email']))
        if not user.exists():
            raise CustomError('User not registered')
        user = user[0]
        if resend_otp(user):
            send_email_otp(user)
        return data


class VerifyOTPEmailSerializer(Serializer):
    email = EmailField()
    otp = IntegerField()

    def validate(self, data):
        user = User.objects.filter(email = normalize_email(data['email']))
        if not user.exists():
            raise CustomError('User not registered')
        user = user[0]
        response = validateOTP(user, data['otp'])
        if response == 'OK':
            return data
        raise CustomError(response)


class ResetPasswordSerializer(Serializer):
    email = EmailField(write_only = True)
    otp = IntegerField(write_only = True)
    password = CharField()

    def validate(self, data):
        if not self.instance.exists():
            raise CustomError('User not registered')
        self.instance = self.instance[0]
        otpresponse = validateOTP(self.instance, data['otp'])
        if not otpresponse == 'OK' :
            raise CustomError('unauthorised access')
        passresponse = validatePASS(data['password'], self.instance.email)
        if not passresponse == 'OK':
            raise CustomError(passresponse)
        validateOTP(self.instance, data['otp'], resetpass = True)
        return data

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance


class SendLINKEmailSerializer(Serializer):
    email = EmailField()
    password = CharField()

    def validate(self, data):
        inemail = normalize_email(data['email'])
        if User.objects.filter(email =inemail).exists():
            raise CustomError('User with this email already exists')
        response = validatePASS(data['password'])
        if not response == 'OK':
            raise CustomError(response)
        tokenobject = SignUpUser.objects.filter(email = inemail)
        if tokenobject.exists():
            if tokenobject[0].token_generated_at + timedelta(minutes=1) > timezone.now():
                raise CustomError('wait for a minute to send another request')
            tokenobject[0].delete()
        send_email_token(data['password'], inemail)
        return data


class VerifyLINKEmailSerializer(Serializer):
    email = EmailField(required = True)
    token = UUIDField(required = True)
    onapp = BooleanField(required=True)

    def validate(self, data):
        email, token = normalize_email(data['email']), data['token']
        object = SignUpUser.objects.filter(email = email)
        tempuser = object[0]
        if not object.exists():
            raise CustomError('Invalid Email')
        if not token == tempuser.token:
            raise CustomError('Invalid Token')
        if tempuser.token_generated_at + timedelta(minutes=15) < timezone.now():
            tempuser.delete()
            raise CustomError('Link Expired')
        if tempuser.is_verified:
            raise CustomError('Link already used')
        return {**data, **{"object" : tempuser}}

    def create(self, validated_data):
        tempuser = validated_data['object']
        tempuser.is_verified = True
        tempuser.save()
        newuser = User.objects.create_user(
            email = normalize_email(tempuser.email),
            name = tempuser.email.split("@")[0],
            password = tempuser.password
        )
        if validated_data['onapp'] :
            return newuser.tokens()
        return {}


class CheckVerificationSerializer(Serializer):
    is_verified = BooleanField(read_only = True, default = False)
    email = EmailField(write_only = True)
    password = CharField(write_only = True)
    access = CharField(read_only = True)
    refresh = CharField(read_only = True)

    def validate(self, data):
        inemail = normalize_email(data['email'])
        object = SignUpUser.objects.filter(email = inemail)
        if not object.exists():
            raise CustomError('Invalid Email')
        object = object[0]
        if not check_password(data['password'], object.password):
            raise CustomError('Unauthorised access')
        if object.is_verified:
            data['is_verified'] = True
            user = authenticate(email=inemail, password=data['password'])
            data['refresh'] = user.refresh
            data['access'] = user.access
            object.delete()
        return data