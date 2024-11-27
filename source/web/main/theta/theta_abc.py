import sys
from abc import ABC, abstractmethod


class ThetaAbstract(ABC):
    modules: dict[str, 'ThetaAbstract'] = {}

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __init_subclass__(cls):
        ThetaAbstract.modules[cls.name] = cls

    @abstractmethod
    def test(self, input:str, expected_output:str):
        ''' Method for checking correct answer '''
        raise NotImplementedError

    @staticmethod
    def _logging(name):
        def decor(func):
            def wrapper(self, *args, **kwargs):
                print("-"*30, name, "-"*30, file=sys.stderr)
                func(self, *args, **kwargs)
                print("-"*28, f'{name} END', "-"*28, file=sys.stderr)
            return wrapper
        return decor