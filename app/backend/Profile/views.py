from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class VerifyPANView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = VerifyPANSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({ **{'message' : ['Verified']}, **serializer.data}, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class NewTwoFactorView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = NewTwoFactorSerializer(data = request.data, context = {'request' : request})
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({'message' : ['OTP sent on your phone number']}, status=status.HTTP_201_CREATED)


class OTPNewTwoFactorView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OTPNewTwoFactorSerializer

    def get_object(self):
        try:
            return self.request.user.twofactor.twofactorotp
        except:
            raise CustomError('raise an OTP first')


class EnableTwoFactorView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnableTwoFactorSerializer

    def get_object(self):
        try:
            return self.request.user.twofactor
        except:
            pass


class DisableTwoFactorView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DisableTwoFactorSerializer

    def get_object(self):
        try:
            return self.request.user.twofactor
        except:
            pass

    def delete(self, request, *args, **kwargs):
        if self.get_object() is None:
            raise CustomError('Two Factor Verification not enabled for this account')
        return super().delete(request, *args, **kwargs)


class ProfilePictureView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfilePictureSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        picture = self.request.user.profile_picture
        if picture != 'profile.jpg':
            picture.delete()
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if user.profile_picture != 'profile.jpg':
            user.profile_picture.delete()
        user.profile_picture = 'profile.jpg'
        user.save()
        return Response({'message' : 'Profile Picture Deleted'})


class UserDetailsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerializer

    def get_object(self):
        return self.request.user