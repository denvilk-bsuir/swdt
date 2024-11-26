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

    def __str__(self):
        return f"#{self.id}/{self.last_name} {self.first_name[:1]}. {self.middle_name[:1]}. ({self.user.username})"
    
    @property
    def fullname(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class Achievment(BaseModel):
    name = models.CharField(max_length=60)
    creator = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"#{self.id} {self.name}"


class UserAchievments(BaseModel):
    achievment = models.ForeignKey(Achievment, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Profile #{self.user.id} get achievment #{self.achievment.id}"


class TaskType(BaseModel):
    name = models.CharField(max_length=40)
    tester_name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Task(BaseModel):
    name = models.CharField(max_length=100)
    task_type = models.ForeignKey(TaskType, null=True, on_delete=models.SET_NULL)
    statement = models.TextField()
    input = models.TextField(null=True, blank=True)
    output = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"#{self.id}/{self.name} ({self.task_type})" 

    @property
    def default_compilers(self):
        return Compiler.objects.all()


class Test(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    test_input = models.TextField(null=True, blank=True)
    test_output = models.TextField()
    order = models.IntegerField()

    def __str__(self):
        return f"Test #{self.order} for {self.task}"


class Verdict(BaseModel):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return f"#{self.id} {self.name}"


class AnswerOption(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="answer_options")
    text = models.CharField(max_length=300)

    def __str__(self):
        return f"Answer Option #{self.id} for {self.task}"


class Compiler(BaseModel):
    name = models.CharField(max_length=30)
    extension = models.CharField(max_length=30)

    def __str__(self):
        return f"#{self.id} {self.name} ({self.extension})"


class AnswerCode(BaseModel):
    code = models.CharField(max_length=30)
    compiler = models.ForeignKey(Compiler, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} ({self.compiler})"


class Answer(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption, null=True, blank=True, on_delete=models.SET_NULL)
    answer_code = models.ForeignKey(AnswerCode, null=True, blank=True, on_delete=models.SET_NULL)
    verdict = models.ForeignKey(Verdict, null=True, on_delete=models.SET_NULL)
    penalty = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer #{self.id} for {self.task}"


class Category(BaseModel):
    category_name = models.CharField(max_length=60)

    def __str__(self):
        return self.category_name


class ContestType(BaseModel):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"#{self.id} {self.name}"


class TaskOnContest(BaseModel):
    order = models.IntegerField()
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task #{self.task.id} to Contest #{self.contest.id} (order #{self.order})"


class CategoryOnContest(BaseModel):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Category #{self.category.id} to Contest #{self.contest.id}"


class CompilerOnContest(BaseModel):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    compiler = models.ForeignKey(Compiler, on_delete=models.CASCADE)

    def __str__(self):
        return f"Compiler #{self.compiler.id} to Contest #{self.contest.id}"


class ContestRole(BaseModel):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class UserToContest(BaseModel):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.ForeignKey(ContestRole, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Profile #{self.user.id} to Contest #{self.contest.id} with role {self.role}"