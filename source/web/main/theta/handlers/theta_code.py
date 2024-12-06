import json
from django.shortcuts import redirect
from main.models import Answer, AnswerCode, Task, Compiler
from main.rmq import rmq_client


def code_answer(request, *args, **kwargs):
    if request.method == 'POST':
        task = Task.objects.get(id=kwargs['id'])
        answer_code = AnswerCode.objects.create(
            code=request.POST.get('answer'),
            compiler=Compiler.objects.get(id=request.POST.get('compiler')),
        )
        answer = Answer.objects.create(
            task=task,
            answer_code=answer_code,
            user=request.user.profile,
            penalty=0,
        )
        data = {
            'task_id': task.id,
            'answer_id': answer.id
        }
        rmq_client.publish(json.dumps(data))

    return redirect(f'/tasks/{kwargs['id']}/')
