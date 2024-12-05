from main.theta.theta_abc import ThetaAbstract
from main.theta.modules.theta_code import ThetaCode


class Theta:

    def __new__(cls, type:str, *args, **kwargs) -> ThetaAbstract:
        _cls = ThetaAbstract.modules.get(type)
        return _cls(*args, **kwargs)