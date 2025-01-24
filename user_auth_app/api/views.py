from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now

from .serializers import RegistrationSerializer, UserProfileSerializer, BusinessUserSerializer, CustomerUserSerializer
from user_auth_app.models import UserProfile
from shared.permissions import IsOwnerOrAdmin


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Function for POST-Requests to register new users. If the request is valid, a Token will be generated for the new User.
        Return value is an object of user data and the token.
        """
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            saved_account.last_login = now()
            saved_account.save(update_fields=['last_login'])
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
            resp_status = status.HTTP_200_OK
        else:
            data = serializer.errors
            resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Function for POST-Requests to authenticate the user and login to the application. If the request is valid, an object of user data and the token will be returned.
        """
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.last_login = now()
            user.save(update_fields=['last_login'])
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id
            }
            resp_status = status.HTTP_200_OK
        else:
            data = serializer.errors
            resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status)


class UserProfileDetailView(RetrieveAPIView, UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrAdmin]
    http_method_names = ['options', 'get', 'patch']


class BusinessUserView(ListAPIView):
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = BusinessUserSerializer


class CustomerUserView(ListAPIView):
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = CustomerUserSerializer
