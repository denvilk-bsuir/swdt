from django.shortcuts import get_object_or_404
from main.models import Answer, Contest, Verdict
from main.theta.theta import Theta

class TaskStandings:

    def __init__(self, type:str):
        self.submissions_count = 0
        self.success = False
        self.penalty = 0

        theta_cls = Theta.get_tester(type)
        self.__task_cls = theta_cls

    def add_answer(self, answer):
        self.__task_cls._set_answer(self, answer)

    def __str__(self) -> str:
        if not self.success and self.submissions_count == 0:
            return ''
        if self.submissions_count == 0:
            return '+' if self.success else '-'
        return f'+{self.submissions_count}' if self.success else f'-{self.submissions_count}'


class UserStanding:

    def __init__(self, task_set, user):
        self.tasks = {}
        self.task_set = task_set
        self.user=user
        for task in task_set:
            self.tasks[task] = TaskStandings(task.task_type.tester_name)

    def add_answer(self, answer: Answer):
        self.tasks[answer.task].add_answer(answer)

    @property
    def penalty(self):
        return sum([task.penalty for task in self.tasks.values()])

    @property
    def total_points(self):
        return sum([1 if task.success else 0 for task in self.tasks.values()])

    def task_results(self):
        return [self.tasks[task] for task in self.task_set]


def create_standings(contest_id):
    _contest = get_object_or_404(Contest, pk=contest_id)

    task_set = []
    for _task_on_contest in _contest.taskoncontest_set.all().order_by('order'):
        task = _task_on_contest.task
        task_set.append(task)

    data = []
    for _user in _contest.users.all():
        user_standings = UserStanding(task_set, _user)
        for task in task_set:
            _answers = Answer.objects.filter(
                user=_user.id,
                task=task.id,
                contest=_contest.id
            ).order_by('created_at')

            for _answer in _answers:
                user_standings.add_answer(_answer)

        data.append(user_standings)
    data.sort(key=lambda x: (-x.total_points, x.penalty))
    return data