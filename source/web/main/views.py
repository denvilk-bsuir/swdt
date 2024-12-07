from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView

from main.forms import LoginForm, SignUpForm
from main.models import Answer, Contest, Task


User = get_user_model()


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request):
        opened_contests = Contest.objects.opened_contests()
        return render(request, self.template_name, {
            'opened_contests': opened_contests,
        })


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


class TaskView(TemplateView):

    def get_task(self, task_id):
        _task = get_object_or_404(Task, pk=task_id)
        self.template_name = f'tasks/{_task.task_type.tester_name}.html'

        return _task

    def get(self, request, *args, **kwargs):
        task = self.get_task(kwargs['id'])
        answers = Answer.objects.filter(task=task, user=request.user.profile).order_by('-created_at')

        return render(request, self.template_name, {'task': task, 'answers': answers})


class TaskListView(TemplateView):
    template_name = 'tasks/tasks_list.html'

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.exclude(contest__in=Contest.objects.active_contests())

        return render(request, self.template_name, {'tasks': tasks})