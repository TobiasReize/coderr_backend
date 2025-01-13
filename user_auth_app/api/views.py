from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken


class RegistrationView(APIView):
    pass


class CustomLoginView(ObtainAuthToken):
    pass
