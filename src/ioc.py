import abc
from collections import defaultdict

from src.command import ICommand, MacroCommand


class IoC(abc.ABC):

    def resolve(self):
        pass


class IoCRegister(ICommand):

    def __init__(self, key, cmd):
        self._cmd = cmd
        self._key = key

    def execute(self):
        IoC.scopes.strategy[self._key] = self._cmd


class Scope:

    def __init__(self):
        self.strategy = defaultdict()
        self.strategy['IoC.Register'] = IoCRegister


class IoC(IoC):

    scopes = Scope()

    @staticmethod
    def resolve(key, *args, **kwargs):
        if IoC.scopes.strategy.get(key):
            return IoC.scopes.strategy[key](*args, **kwargs)
        else:
            raise ValueError
