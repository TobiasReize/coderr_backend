from django.urls import path
from .views import RegistrationView, CustomLoginView, UserProfileDetailView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),
    # path('profiles/business/'),
    # path('profiles/customers/'),
]
