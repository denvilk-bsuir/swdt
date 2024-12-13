from django.core.management.base import BaseCommand

from main.models import (
    Compiler,
    ContestRole,
    TaskType,
    Verdict,
)

class Command(BaseCommand):
    help = 'Initialize models'

    def handle(self, *args, **options):
        Compiler.objects.get_or_create(name="GNU C++20", extension='.cpp20')

        TaskType.objects.get_or_create(name='Code', tester_name='theta_code')
        TaskType.objects.get_or_create(name='Quiz', tester_name='theta_quiz')

        Verdict.objects.get_or_create(name='OK', short_name='ok')
        Verdict.objects.get_or_create(name='Wrong answer', short_name='wa')
        Verdict.objects.get_or_create(name='Time limit exceeded', short_name='tl')
        Verdict.objects.get_or_create(name='Memory limit exceeded', short_name='ml')
        Verdict.objects.get_or_create(name='Runtime error', short_name='re')
        Verdict.objects.get_or_create(name='Fail', short_name='fail')
        Verdict.objects.get_or_create(name='Presentation error', short_name='pe')
        Verdict.objects.get_or_create(name='Compilation error', short_name='ce')
        Verdict.objects.get_or_create(name='Error', short_name='err')

        ContestRole.objects.get_or_create(name='Participant')