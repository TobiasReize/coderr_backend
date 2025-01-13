from django.urls import path
from .views import RegistrationView, CustomLoginView


urlpatterns = [
    # path('profile/', UserProfileList.as_view(), name='userprofile-list'),     # eine View um alle Profile anzuzeigen?
    # path('profile/<int:pk>/'),
    # path('profiles/business/'),
    # path('profiles/customers/'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
