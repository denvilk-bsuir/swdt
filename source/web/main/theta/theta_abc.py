import sys
from enum import Enum
from abc import ABC, abstractmethod


class ThetaAbstract(ABC):
    modules: dict[str, 'ThetaAbstract'] = {}

    class TaskResultVerdict(Enum):
        OK = 'ok'
        WA = 'wa'
        CE = 'ce'
        RE = 're'
        PE = 'pe'
        FAIL = 'fail'
        ML = 'ml'
        TL = 'tl'
        ERR = 'err'

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
                res = func(self, *args, **kwargs)
                print("-"*28, f'{name} END', "-"*28, file=sys.stderr)
                return res
            return wrapper
        return decor