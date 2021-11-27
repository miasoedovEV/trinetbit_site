from django.urls import path
from .views import *

urlpatterns = [
    path('login', MyLoginView.as_view(), name='login'),
    path('logout', MyLogoutView.as_view(), name='logout'),
    path('personal_account', ProfileView.as_view(), name='personal_account'),
    path('register', RegisterView.as_view(), name='register'),
    path('verification', VerificationView.as_view(), name='verification'),
]