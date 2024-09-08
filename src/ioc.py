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

class IoCRegistry(AbsFactory):

    def __init__(self, ):
        pass

    def create_service(self):
        return lambda x:print( x)

class IoC(abc.ABC):

    def resolve(self):
        pass


class IoCResolver(IoC):



    def __init__(self):
        self._strategy = defaultdict(ICommand)
        self._strategy['register'] = self.register_factory

    def resolve_cmd(self, key, *args, **kwargs):
        # self._strategy[key].create_service(*args, **kwargs)
        if self._strategy.get(key):
            return self._strategy[key](*args, **kwargs)
        else:
            raise ValueError

    def resolve_factory(self, key, *args, **kwargs):
        if self._strategy.get(key):
            return self._strategy[key](*args, **kwargs).create_service()
        else:
            raise ValueError

    def register_factory(self, key, factory):
        self._strategy[key] = factory

    def resolve(self, key, *args, **kwargs):
        return self.resolve_cmd(key, *args, **kwargs)
