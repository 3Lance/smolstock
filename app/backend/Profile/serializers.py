from rest_framework.serializers import Serializer, ModelSerializer, EmailField, CharField, IntegerField
from Authentication.models import User, Two_Factor_Verification, Two_Factor_OTP
from Authentication.utils import CustomError, normalize_email, validatePASS
from django.contrib.auth.hashers import make_password, check_password
from .models import PAN_Verification
from rest_framework import status
from Authentication.utils import validateOTP, send_two_factor_otp


class VerifyPANSerializer(ModelSerializer):
    email = EmailField()
    name = CharField(required = False, allow_null = True, default = None)
    
    class Meta:
        model = PAN_Verification
        fields = ['email', 'pan_number', 'name']
        extra_kwargs = {'pan_number': {'required': False, 'allow_null': True, 'default':None}}

    def validate(self, data):
        data['email'] = normalize_email(data['email'])
        user = User.objects.filter(email = data['email'])
        if user.exists():
            if data['pan_number'] is None:
                return data
            if PAN_Verification.objects.filter(user = user[0]).exists():
                raise CustomError('User already verified')
            return data
        raise CustomError('User not registered')
    
    def create(self, validated_data):
        holder = User.objects.get(email = validated_data['email'])
        if validated_data['pan_number'] is not None:
            PAN_Verification(
                user = holder,
                pan_number = validated_data['pan_number']
            ).save()

        if validated_data['name'] is not None:
            holder.name = validated_data['name']
            holder.save()
        return validated_data


class ChangePasswordSerializer(ModelSerializer):
    newpassword = CharField(max_length=128, write_only = True, required = True)

    class Meta:
        model = User
        fields = ['password', 'newpassword']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def validate(self, data):
        if not check_password(data['password'], self.instance.password):
            raise CustomError("Incorrect previous password", code=status.HTTP_406_NOT_ACCEPTABLE)

        if check_password(data['newpassword'], self.instance.password):
            raise CustomError("Password same as previous password", code=status.HTTP_406_NOT_ACCEPTABLE)

        passresponse = validatePASS(data['newpassword'])
        if not passresponse == 'OK':
            raise CustomError(passresponse)

        return data

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['newpassword'])
        instance.save()
        return validated_data

    def to_representation(self, instance):
        return {'message':['Password changed successfully']}


class NewTwoFactorSerializer(Serializer):
    phone_number = IntegerField(max_value = 9999999999, min_value = 1000000000)

    def validate(self, data):
        user = self.context['request'].user
        try:
            obj = user.twofactor
        except:
            if Two_Factor_Verification.objects.filter(phone_number = data['phone_number']).exists():
                raise CustomError('Phone number already in use', code = status.HTTP_226_IM_USED)
            data['user'] = user
        else:
            if obj.verified:
                raise CustomError('Two Factor verification already exists for this account', code = status.HTTP_409_CONFLICT)
            raise CustomError('Verify your phone number to enable two factor verification', code = status.HTTP_403_FORBIDDEN)
        return data

    def create(self, validated_data):
        obj = Two_Factor_Verification.objects.create(
            user = validated_data['user'],
            phone_number = validated_data['phone_number']
        )
        send_two_factor_otp(obj)


class OTPNewTwoFactorSerializer(Serializer):
    otp = IntegerField(max_value = 9999, min_value = 1000)

    def validate(self, data):
        user = self.context['request'].user
        data['obj'] = self.instance
        response = validateOTP(user, data['otp'], twofactoron=True)
        if response != 'OK':
            raise CustomError(response)
        return data

    def update(self, instance, validated_data):
        obj = validated_data['obj'].phone_number
        obj.verified = True
        obj.enabled = True
        obj.save()
        return {}

    def to_representation(self, instance):
        return {'message' : ['Two Factor Verification Enabled for this account']}


class EnableTwoFactorSerializer(ModelSerializer):
    class Meta:
        model = Two_Factor_Verification
        fields = ['enabled']

    def validate(self, instance):
        try:
            obj = self.context['request'].user.twofactor
        except:
            raise CustomError('Two Factor Verification not enabled for this account')
        if obj.verified:
            return {'do' : True}
        raise CustomError('Two Factor Verification not verified for this account')

    def update(self, instance, validated_data):
        if validated_data['do']:
            instance.enabled = True
        return super().update(instance, validated_data)


class DisableTwoFactorSerializer(ModelSerializer):
    class Meta:
        model = Two_Factor_Verification
        fields = ['enabled']
 
    def validate(self, instance):
        try:
            self.context['request'].user.twofactor
        except:
            raise CustomError('Two Factor Verification not enabled for this account')
        return {}

    def update(self, instance, validated_data):
        instance.enabled = False
        return super().update(instance, validated_data)


class ProfilePictureSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_picture']
        extra_kwargs = {'profile_picture': {'required': True}}


class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'profile_picture']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['two_factor_verification'] = False
        try:
            obj = instance.twofactor
            if obj.verified:
                if obj.enabled:
                    data['two_factor_verification'] = True
                data['phone_number'] = obj.phone_number
        except:
            pass

        try:
            obj = instance.pan_details
            data['pan_verification'] = True
            data['pan_number'] = obj.pan_number
            data['walltet'] = instance.wallet.amount
        except:
            data['pan_verification'] = False

        return data