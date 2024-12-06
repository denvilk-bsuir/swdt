from main.models import Answer
from main.theta.theta_abc import ThetaAbstract


class ThetaQuiz(ThetaAbstract):
    name = 'theta_quiz'
    test_result = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.answer: Answer = kwargs.get('answer')

    @ThetaAbstract._logging("TEST")
    def test(self, expected_output, input=None):
        self.test_result = (
            ThetaAbstract.TaskResultVerdict.OK
            if expected_output == str(self.answer.answer_option.text)
            else ThetaAbstract.TaskResultVerdict.WA
        )