import sys
import json

from django.core.management.base import BaseCommand

from main.models import Answer
from main.theta.theta import Theta
from main.rmq import rmq_client

class Command(BaseCommand):
    help = 'Runner for tester tasks'

    @staticmethod
    def rmq_callback(ch, method, properties, body):
        data = json.loads(body.decode())
        answer = Answer.objects.get(id=data['answer_id'])
        tester = Theta(answer.task.task_type.tester_name, answer=answer, task=answer.task)

        for test in answer.task.test_set.all():
            tester.test(
                input=test.test_input,
                expected_output=test.test_output,
            )

        print(tester.test_result, file=sys.stderr)
        # ch.basic_ack(delivery_tag = method.delivery_tag)

    def handle(self, *args, **options):
        # answer = Answer.objects.get(id=7) # quiz
        rmq_client.consume(self.rmq_callback)