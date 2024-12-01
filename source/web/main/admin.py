from django.contrib import admin
from main.models import (
    Profile, 
    Achievment, 
    UserAchievments, 
    TaskType, 
    Task, 
    Test, 
    Verdict, 
    AnswerOption, 
    Compiler, 
    AnswerCode, 
    Answer, 
    Category, 
    ContestType, 
    Contest, 
    TaskOnContest, 
    CategoryOnContest,
    CompilerOnContest, 
    ContestRole, 
    UserToContest,
    Checker,
)


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    class Meta:
        abstract = True


@admin.register(Profile)
class ProfileAdmin(BaseAdmin):
    list_display = [
        'id',
        'user',
        'first_name',
        'middle_name',
        'last_name',
        'country',
        'email',
        'rating'
    ]


@admin.register(Achievment)
class AchievmentAdmin(BaseAdmin):
    list_display = [
        'id',
        'name',
        'creator'
    ]


@admin.register(UserAchievments)
class UserAchievmentsAdmin(BaseAdmin):
    list_display = [
        'id',
        'achievment',
        'user'
    ]


@admin.register(TaskType)
class TaskTypeAdmin(BaseAdmin):
    list_display = [
        'id',
        'name',
        'tester_name'
    ]


@admin.register(Task)
class TaskAdmin(BaseAdmin):
    list_display = [
        'id',
        'name',
        'task_type',
        'statement',
        'input',
        'output',
        'note'
    ]


@admin.register(Test)
class TestAdmin(BaseAdmin):
    list_display = [
        'id',
        'task',
        'test_input',
        'test_output',
        'order'
    ]


@admin.register(Verdict)
class VerdictAdmin(BaseAdmin):
    list_display = [
        'id',
        'name',
        'short_name'
    ]


@admin.register(AnswerOption)
class AnswerOptionAdmin(BaseAdmin):
    list_display = [
        'id',
        'task',
        'text'
    ]


@admin.register(Compiler)
class CompillerAdmin(BaseAdmin):
    list_display = [
        'id',
        'name',
        'extension'
    ]


@admin.register(AnswerCode)
class AnswerCodeAdmin(BaseAdmin):
    list_display = [
        'id',
        'code',
        'compiler'
    ]


@admin.register(Answer)
class AnswerAdmin(BaseAdmin):
    list_display = [
        'id',
        'task',
        'answer_option',
        'answer_code',
        'verdict',
        'penalty'
    ]


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = [
        'id',
        'category_name'
    ]


@admin.register(ContestType)
class ContestTypeAdmin(BaseAdmin):
    list_display = [
        'id',
        'name',
        'description'
    ]


@admin.register(Contest)
class ContestAdmin(BaseAdmin):
    list_display = [
        'id',
        'author',
        'start_time',
        'duration',
        'name',
        'type'
    ]


@admin.register(TaskOnContest)
class TaskOnContest(BaseAdmin):
    list_display = [
        'id',
        'order',
        'contest',
        'task'
    ]


@admin.register(CategoryOnContest)
class CategoryOnContestAdmin(BaseAdmin):
    list_display = [
        'id',
        'contest',
        'category'
    ]


@admin.register(CompilerOnContest)
class CompilerOnContestAdmin(BaseAdmin):
    list_display = [
        'id',
        'contest',
        'compiler'
    ]


@admin.register(ContestRole)
class ContestRoleAdmin(BaseAdmin):
    list_display = [
        'id',
        'name'
    ]


@admin.register(UserToContest)
class UserToContestAdmin(BaseAdmin):
    list_display = [
        'id',
        'contest',
        'user',
        'role'
    ]

@admin.register(Checker)
class CheckerAdmin(BaseAdmin):
    list_display = [
        'id',
        'compiler',
        'code'
    ]