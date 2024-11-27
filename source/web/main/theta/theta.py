from main.theta.theta_abc import ThetaAbstract

class Theta:

    def __new__(cls, type:str, *args, **kwargs) -> ThetaAbstract:
        _cls = ThetaAbstract.modules.get(type)
        return _cls(*args, **kwargs)