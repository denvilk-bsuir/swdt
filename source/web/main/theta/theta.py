from main.theta.theta_abc import ThetaAbstract
from main.theta.modules.theta_code import ThetaCode
from main.theta.modules.theta_quiz import ThetaQuiz


class Theta:

    def __new__(cls, type:str, *args, **kwargs) -> ThetaAbstract:
        _cls = Theta.get_tester(type)
        return _cls(*args, **kwargs)

    @staticmethod
    def get_tester(type:str):
        return ThetaAbstract.modules.get(type)
