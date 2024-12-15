from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView

from main.forms import LoginForm, SignUpForm
from main.models import (
    Answer,
    Contest,
    ContestRole,
    Task,
    UserToContest,
    TaskOnContest,
)


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
    template_name = 'tasks/task_detail.html'

    def get_task(self, task_id):
        _task = get_object_or_404(Task, pk=task_id)
        self.task_template_name = f'tasks/{_task.task_type.tester_name}.html'

        return _task

    def get(self, request, *args, **kwargs):
        task = self.get_task(kwargs['id'])
        answers = Answer.objects.filter(task=task, user=request.user.profile).order_by('-created_at')

        return render(
            request,
            self.template_name,
            {
                'task': task,
                'answers': answers,
                'task_template':self.task_template_name,
            }
        )


class TaskListView(TemplateView):
    template_name = 'tasks/tasks_list.html'

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.exclude(contest__in=Contest.objects.active_contests())

        return render(request, self.template_name, {'tasks': tasks})


class ContestListView(TemplateView):
    template_name = 'contests/contests_list.html'

    def get(self, request, *args, **kwargs):
        contests = Contest.objects.all().order_by('-start_time')
        return render(request, self.template_name, {'contests': contests})


class ContestRegisterView(TemplateView):
    template_name = 'contests/registration.html'

    def get_contest(self, contest_id):
        return get_object_or_404(Contest, pk=contest_id)

    def get(self, request, *args, **kwargs):
        contest = self.get_contest(kwargs['id'])
        if contest not in Contest.objects.opened_contests():
            return redirect('index')
        if request.user.profile in contest.users.all():
            return redirect('contest_detail', kwargs['id'])
        return render(request, self.template_name, {'contest': self.get_contest(kwargs['id'])})

    def post(self, request, *args, **kwargs):
        contest = self.get_contest(kwargs['id'])
        if contest in Contest.objects.opened_contests() and\
            request.user.profile not in contest.users.all():
                UserToContest.objects.create(
                    contest=contest,
                    user=request.user.profile,
                    role=ContestRole.objects.get(name="Participant")
                )
                return redirect('contest_detail', kwargs['id'])
        return render(request, self.template_name, {'contest': contest})


class ContestDetailView(TemplateView):
    template_name = 'contests/contest_detail.html'

    def get_contest(self, contest_id):
        return get_object_or_404(Contest, pk=contest_id)

    def get(self, request, *args, **kwargs):
        contest = self.get_contest(kwargs['id'])
        return render(
            request,
            self.template_name,
            {
                'tasks': contest.tasks,
                'contest': contest,
            }
        )


class ContestTaskView(TemplateView):
    template_name = 'contests/contest_task.html'

    def get(self, request, *args, **kwargs):
        task_on_contest = get_object_or_404(
            TaskOnContest,
            contest__id=kwargs['id'],
            order=kwargs['task_order']
        )
        task = task_on_contest.task
        contest = task_on_contest.contest

        template_name = f'tasks/{task.task_type.tester_name}.html'

        return render(
            request,
            self.template_name,
            {
                'task_template': template_name,
                'task': task,
                'contest': contest,
            }
        )


class ContestStandingsView(TemplateView):
    template_name = "contests/contest_standings.html"

    def get_contest(self, contest_id):
        return get_object_or_404(Contest, pk=contest_id)

    def create_code_table(self, contest_id):
        _contest = self.get_contest(contest_id)

        data = []

        for _user in _contest.users.all():

            user_penalty = 0
            user_balls = 0
            tasks_res = []
            for _task_on_contest in _contest.taskoncontest_set.all().order_by('order'):
                _task = _task_on_contest.task
                task_posts = 0
                _answers = Answer.objects.filter(
                    user=_user.id,
                    task=_task.id,
                    contest=_contest.id
                ).order_by('created_at')
                if not _answers:
                    tasks_res.append('-')
                else:
                    for _answer in _answers:
                        good_end = False
                        if _answer.verdict:
                            if _answer.verdict.short_name == "ok":
                                user_balls += 1
                                dt = _answer.created_at - _contest.start_time
                                mins_penalty = dt // 60
                                user_penalty += task_posts*20 + mins_penalty
                                task_posts += 1
                                good_end = True
                                break
                            else:
                                task_posts += 1
                    if good_end:
                        tasks_res.append(f'+{task_posts}')
                    else:
                        tasks_res.append(f'-{task_posts if task_posts > 0 else ''}')
            data.append((_user.__str__,user_balls,user_penalty,tasks_res))
        data.sort(key=lambda x: (-x[1], x[2]))
        return data

    def get(self, request, *args, **kwargs):

        _contest = get_object_or_404(Contest, pk = kwargs["id"])

        _data = self.create_code_table(kwargs["id"])
        return render(
            request,
            self.template_name,
            {
                "results": _data,
                "contest": _contest
            }
        )