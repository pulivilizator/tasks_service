from django.urls import path

from . import views

app_name = 'authentication'


urlpatterns = [
    path('api/token/refresh/', views.TokenRefreshSchemaView.as_view(), name='token_refresh'),
    path('auth/registration/', views.RegistrationAPIView.as_view(), name='registration'),
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='logout'),
]
