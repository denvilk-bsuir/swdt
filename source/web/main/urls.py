from django.urls import path
from main.views import SignUpView, index, login

urlpatterns = [
    path("", index),
    path("users/signup/", SignUpView.as_view(), name="signup"),
    path("users/login/", login, name="login"),
]
