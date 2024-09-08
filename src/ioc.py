import abc
from collections import defaultdict

from src.command import ICommand, MacroCommand


class AbsFactory(abc.ABC):

    def create_service(self, service, *args, **kwargs):
        pass


class MacroCmdFactory(AbsFactory):

    def __init__(self, cmds):
        self._cmds = cmds

    def create_service(self):
        return MacroCommand(self._cmds)


class IoC(abc.ABC):

    def resolve(self):
        pass


class IoCResolver(IoC):

    def __init__(self):
        self._strategy = defaultdict(ICommand)

    def resolve_cmd(self, key, *args, **kwargs):
        # self._strategy[key].create_service(*args, **kwargs)
        return self._strategy[key](*args, **kwargs)

    def resolve_factory(self, key, *args, **kwargs):
        if self._strategy.get(key):
            return self._strategy[key](*args, **kwargs).create_service()
        else:
            self._strategy[key] = args[0]

    def register_factory(self, key, factory):
        self._strategy[key] = factory

    def resolve(self, key, *args, **kwargs):
        return self.resolve_cmd(key, *args, **kwargs)
