from django.db import models
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    country = models.CharField(max_length=40)
    email = models.CharField(max_length=80)
    rating = models.IntegerField(default=0)
    achievments = models.ManyToManyField('Achievment', through='UserAchievments')


class Achievment(BaseModel):
    name = models.CharField(max_length=60)
    creator = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)


class UserAchievments(BaseModel):
    achievment = models.ForeignKey(Achievment, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

class TaskType(BaseModel):
    name = models.CharField(max_length=40)
    tester_name = models.CharField(max_length=40)


class Task(BaseModel):
    name = models.CharField(max_length=100)
    task_type = models.ForeignKey(TaskType, null=True, on_delete=models.SET_NULL)
    statement = models.CharField(max_length=400)
    input = models.CharField(max_length=400, null=True, blank=True)
    output = models.CharField(max_length=400, null=True, blank=True)
    note = models.CharField(max_length=400, null=True, blank=True)


class Test(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    test_input = models.TextField(null=True, blank=True)
    test_output = models.TextField()


class Verdict(BaseModel):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)


class AnswerOption(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)


class Compiler(BaseModel):
    name = models.CharField(max_length=30)
    extension = models.CharField(max_length=30)


class AnswerCode(BaseModel):
    code = models.CharField(max_length=30)
    compiler = models.ForeignKey(Compiler, on_delete=models.CASCADE)


class Answer(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption,null=True, blank=True, on_delete=models.SET_NULL)
    answer_code = models.ForeignKey(AnswerCode,null=True, blank=True, on_delete=models.SET_NULL)
    verdict = models.ForeignKey(Verdict,null=True, on_delete=models.SET_NULL)
    penalty = models.IntegerField()


class Category(BaseModel):
    category_name = models.CharField(max_length=60)


class ContestType(BaseModel):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)


class Contest(BaseModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='authored_contests')
    start_time = models.DateTimeField()
    duration = models.DurationField()
    name = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task, through='TaskOnContest')
    categories = models.ManyToManyField(Category, through='CategoryOnContest')
    compilers = models.ManyToManyField(Compiler, through='CompilerOncontest')
    users = models.ManyToManyField(Profile, through='UserToContest', related_name='contests')
    type = models.ForeignKey(ContestType, on_delete=models.SET_NULL, null=True, blank=True)


class TaskOnContest(BaseModel):
    order = models.IntegerField()
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class CategoryOnContest(BaseModel):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class CompilerOnContest(BaseModel):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    compiler = models.ForeignKey(Compiler, on_delete=models.CASCADE)


class ContestRole(BaseModel):
    name = models.CharField(max_length=40)


class UserToContest(BaseModel):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.ForeignKey(ContestRole, null=True, on_delete=models.SET_NULL)