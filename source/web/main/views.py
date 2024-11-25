from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.views import LoginView

from main.forms import LoginForm, SignUpForm


User = get_user_model()


def index(request):
    return render(request, 'main/index.html')


class SignUpView(TemplateView):
    template_name = 'main/users/signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
                form.add_error('password_confirm', 'Пароли не совпадают')
                return render(request, self.template_name, {'form': form})

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )

            user.profile.first_name = form.cleaned_data['first_name']
            user.profile.middle_name = form.cleaned_data['middle_name']
            user.profile.last_name = form.cleaned_data['last_name']
            user.profile.country = form.cleaned_data['country']
            user.profile.save()

            return redirect('login')
        return render(request, self.template_name, {'form': form})


class UserLoginView(LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'main/users/login.html'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data.update({
            'form': self.get_form()
        })
        return data

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

def login(request):
    return render(request, 'test.html')