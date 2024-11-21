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



class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']

    class Meta:
        abstract = True


#admin.site.register(Profile)
@admin.register(Profile)
class ProfileAdmin(BaseAdmin):
    list_display = ['id','user','first_name','middle_name','last_name','country','email','rating']


#admin.site.register(Achievment)
@admin.register(Achievment)
class AchievmentAdmin(BaseAdmin):
    list_display = ['id','name','creator']


#admin.site.register(UserAchievments)
@admin.register(UserAchievments)
class UserAchievmentsAdmin(BaseAdmin):
    list_display = ['id','achievment','user']


#admin.site.register(TaskType)
@admin.register(TaskType)
class TaskTypeAdmin(BaseAdmin):
    list_display = ['id','name','tester_name']


#admin.site.register(Task)
@admin.register(Task)
class TaskAdmin(BaseAdmin):
    list_display = ['id','name','task_type','statement','input','output','note']


#admin.site.register(Test)
@admin.register(Test)
class TestAdmin(BaseAdmin):
    list_display = ['id','task','test_input','test_output','order']


#admin.site.register(Verdict)
@admin.register(Verdict)
class VerdictAdmin(BaseAdmin):
    list_display = ['id','name','short_name']


#admin.site.register(AnswerOption)
@admin.register(AnswerOption)
class AnswerOptionAdmin(BaseAdmin):
    list_display = ['id','task','text']


#admin.site.register(Compiler)
@admin.register(Compiler)
class CompillerAdmin(BaseAdmin):
    list_display = ['id','name','extension']


#admin.site.register(AnswerCode)
@admin.register(AnswerCode)
class AnswerCodeAdmin(BaseAdmin):
    list_display = ['id','code','compiler']


#admin.site.register(Answer)
@admin.register(Answer)
class AnswerAdmin(BaseAdmin):
    list_display = ['id','task','answer_option','answer_code','verdict','penalty']


#admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ['id','category_name']


#admin.site.register(ContestType)
@admin.register(ContestType)
class ContestTypeAdmin(BaseAdmin):
    list_display = ['id','name','description']


#admin.site.register(Contest)
@admin.register(Contest)
class ContestAdmin(BaseAdmin):
    list_display = ['id','author','start_time','duration','name','type']


#admin.site.register(TaskOnContest)
@admin.register(TaskOnContest)
class TaskOnContest(BaseAdmin):
    list_display = ['id','order','contest','task']


#admin.site.register(CategoryOnContest)
@admin.register(CategoryOnContest)
class CategoryOnContestAdmin(BaseAdmin):
    list_display = ['id','contest','category']


#admin.site.register(CompilerOnContest)
@admin.register(CompilerOnContest)
class CompilerOnContestAdmin(BaseAdmin):
    list_display = ['id','contest','compiler']


#admin.site.register(ContestRole)
@admin.register(ContestRole)
class ContestRoleAdmin(BaseAdmin):
    list_display = ['id','name']


#admin.site.register(UserToContest)
@admin.register(UserToContest)
class UserToContestAdmin(BaseAdmin):
    list_display = ['id','contest','user','role']