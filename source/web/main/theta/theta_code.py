from django.shortcuts import redirect
from main.models import Answer, AnswerCode, Task, Compiler


def code_answer(request, *args, **kwargs):
    if request.method == 'POST':
        task = Task.objects.get(id=kwargs['id'])
        answer_code = AnswerCode.objects.create(
            code=request.POST.get('answer'),
            compiler=Compiler.objects.get(id=request.POST.get('compiler')),
        )
        Answer.objects.create(
            task=task,
            answer_code=answer_code,
            user=request.user.profile,
            penalty=0,
        )

    return redirect(f'/tasks/{kwargs['id']}/')
