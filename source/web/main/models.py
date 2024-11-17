from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    country = models.CharField(max_length=40)
    email = models.CharField(max_length=80)
    raiting = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    achievments = models.ManyToManyField('Achievment', through='UserAchievments')


class Achievment(models.Model):
    name = models.CharField(max_length=60)
    creator = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
   
class UserAchievments(models.Model):
    achievment = models.ForeignKey(Achievment, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskType(models.Model):
    name = models.CharField(max_length=40)
    tester_name = models.CharField(max_length=40)


class Task(models.Model):
    task_type = models.ForeignKey(TaskType, null=True, on_delete=models.SET_NULL)
    statement = models.CharField(max_length=400)
    input = models.CharField(max_length=400, null=True, blank=True)
    output = models.CharField(max_length=400, null=True, blank=True)
    note = models.CharField(max_length=400, null=True, blank=True)


class Test(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    test_input = models.TextField(null=True, blank=True)
    test_output = models.TextField()


class Verdict(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)


class AnswerOption(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)


class Compiller(models.Model):
    name = models.CharField(max_length=30)
    extension = models.CharField(max_length=30)


class AnswerCode(models.Model):
    code = models.CharField(max_length=30)
    compiler = models.ForeignKey(Compiller, on_delete=models.CASCADE)


class Answer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption,null=True, blank=True, on_delete=models.SET_NULL)
    answer_code = models.ForeignKey(AnswerCode,null=True, blank=True, on_delete=models.SET_NULL)
    verdict = models.ForeignKey(Verdict,null=True, on_delete=models.SET_NULL)
    penalty = models.IntegerField()


class Category(models.Model):
    category_name = models.CharField(max_length=60)


class ContestType(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)


class Contest(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration = models.DurationField()
    name = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task, through='TaskOnContest')
    categories = models.ManyToManyField(Category, through='CategoryOnContest')
    compillers = models.ManyToManyField(Compiller, through='CompillerOncontest')
    users = models.ManyToManyField(Profile, through='UserToContest')


class TaskOnContest(models.Model):
    order = models.IntegerField()
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class CategoryOnContest(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class CompillerOncontest(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    compiller = models.ForeignKey(Compiller, on_delete=models.CASCADE)


class ContestRole(models.Model):
    name = models.CharField(max_length=40)


class UserToContest(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.ForeignKey(ContestRole, null=True, on_delete=models.NU)