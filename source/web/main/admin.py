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
)

# Register your models here.
admin.site.register(Profile)
admin.site.register(Achievment)
admin.site.register(UserAchievments)
admin.site.register(TaskType)
admin.site.register(Task)
admin.site.register(Test)
admin.site.register(Verdict)
admin.site.register(AnswerOption)
admin.site.register(Compiler)
admin.site.register(AnswerCode)
admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(ContestType)
admin.site.register(Contest)
admin.site.register(TaskOnContest)
admin.site.register(CategoryOnContest)
admin.site.register(CompilerOnContest)
admin.site.register(ContestRole)
admin.site.register(UserToContest)