from django.urls import path
from .views import RegistrationView, CustomLoginView, UserProfileDetailView, BusinessUserView, CustomerUserView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),
    path('profiles/business/', BusinessUserView.as_view(), name='business-user'),
    path('profiles/customer/', CustomerUserView.as_view(), name='customer-user')
]
