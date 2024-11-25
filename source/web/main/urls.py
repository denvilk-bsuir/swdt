from django.urls import path
from django.contrib.auth.views import LogoutView
from main.views import SignUpView, index, UserLoginView


urlpatterns = [
    path("", index, name='index'),
    path("users/logout/", LogoutView.as_view(), name="logout"),
    path("users/signup/", SignUpView.as_view(), name="signup"),
    path("users/login/", UserLoginView.as_view(), name="login"),
]
