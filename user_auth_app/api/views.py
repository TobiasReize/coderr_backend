from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.timezone import now

from .serializers import RegistrationSerializer, UserProfileUpdateSerializer, UserProfileRetrieveSerializer
from user_auth_app.models import UserProfile
from shared.permissions import IsOwnerOrAdmin


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
        else:
            data = serializer.errors
        return Response(data)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
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
        else:
            data = serializer.errors

        return Response(data)


class UserProfileDetailView(RetrieveAPIView, UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return UserProfileUpdateSerializer
        else:
            return UserProfileRetrieveSerializer
