from django.urls import path
from .views import RegistrationView, CustomLoginView


urlpatterns = [
    # path('profile/<int:pk>/'),
    # path('profiles/business/'),
    # path('profiles/customers/'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
