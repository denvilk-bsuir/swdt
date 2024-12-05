from django.urls import path
from django.contrib.auth.views import LogoutView
from main.views import (
    IndexView,
    SignUpView,
    TaskView,
    UserLoginView,
)
from main.theta.handlers.theta_code import code_answer

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path("users/logout/", LogoutView.as_view(), name="logout"),
    path("users/signup/", SignUpView.as_view(), name="signup"),
    path("users/login/", UserLoginView.as_view(), name="login"),

    path('tasks/<int:id>/', TaskView.as_view(), name='theta_task'),

    path('tasks/<int:id>/theta_code', code_answer, name='theta_code'),
]
