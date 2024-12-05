import json
from django.shortcuts import redirect
from main.models import Answer, Task, AnswerOption
from main.rmq import rmq_client


def quiz_answer(request, *args, **kwargs):
    if request.method == 'POST':
        task = Task.objects.get(id=kwargs['id'])
        answer_option = AnswerOption.objects.get(id=request.POST.get('answer'))
        answer = Answer.objects.create(
            task=task,
            answer_option=answer_option,
            user=request.user.profile,
            penalty=0,
        )
        data = {
            'task_id': task.id,
            'answer_id': answer.id
        }
        rmq_client.publish(json.dumps(data))

    return redirect(f'/tasks/{kwargs['id']}/')
