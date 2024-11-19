from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from main.forms import SignUpForm


User = get_user_model()


def index(request):
    return render(request, 'main/index.html')


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'main/users/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
                form.add_error('password_confirm', 'Пароли не совпадают')
                return render(request, 'main/users/signup.html', {'form': form})

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
        return render(request, 'main/users/signup.html', {'form': form})

def login(request):
    return render(request, 'test.html')