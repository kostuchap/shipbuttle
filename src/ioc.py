import abc
from collections import defaultdict

from src.command import ICommand, MacroCommand

class IoC(abc.ABC):

    def resolve(self):
        pass


class IoCResolver(IoC):

    def __init__(self):
        self._strategy = defaultdict(ICommand)
        self._strategy['register'] = self._register_factory

    def _resolve_cmd(self, key, *args, **kwargs):
        if self._strategy.get(key):
            return self._strategy[key](*args, **kwargs)
        else:
            raise ValueError

    def _register_factory(self, key, factory):
        self._strategy[key] = factory

    def resolve(self, key, *args, **kwargs):
        return self._resolve_cmd(key, *args, **kwargs)
