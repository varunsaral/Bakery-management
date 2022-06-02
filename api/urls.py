from django.urls import path
from .views import UserLogin,UserRegister
urlpatterns = [
    path('user/register/',UserRegister.as_view(),name="register"),
    path('user/login/',UserLogin.as_view(),name="login")
]
