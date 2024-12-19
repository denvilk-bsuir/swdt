from main.models import Answer, Verdict
from main.theta.theta_abc import ThetaAbstract


class ThetaQuiz(ThetaAbstract):
    name = 'theta_quiz'
    test_result = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.answer: Answer = kwargs.get('answer')

    @staticmethod
    def answer_result(self, answer: Answer):
        if self.success:
            return
        if answer.verdict and answer.verdict == Verdict.objects.get(short_name='ok'):
            self.success = True
            penalty_delta = answer.created_at - answer.contest.start_time
            self.penalty = penalty_delta.seconds // 60
            return

    @ThetaAbstract._logging("TEST")
    def test(self, expected_output, input=None):
        self.test_result = (
            ThetaAbstract.TaskResultVerdict.OK
            if expected_output == str(self.answer.answer_option.text)
            else ThetaAbstract.TaskResultVerdict.WA
        )