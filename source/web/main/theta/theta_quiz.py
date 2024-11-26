from django.shortcuts import redirect
from main.models import Answer, Task, AnswerOption


def quiz_answer(request, *args, **kwargs):
    if request.method == 'POST':
        task = Task.objects.get(id=kwargs['id'])
        answer_option = AnswerOption.objects.get(id=request.POST.get('answer'))
        Answer.objects.create(
            task=task,
            answer_option=answer_option,
            user=request.user.profile,
            penalty=0,
        )

    return redirect(f'/tasks/{kwargs['id']}/')
