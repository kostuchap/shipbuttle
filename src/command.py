from abc import ABC, abstractmethod

class ICommand(ABC):

    @abstractmethod
    def execute(self):
        pass


class MacroCommand(ICommand):

    def __init__(self, cmds: list):
        self._cmds = cmds

    def execute(self):
        for cmd in self._cmds:
            cmd.execute()


class LambdaCommand(ICommand):

    def __init__(self, lmbd):
        self._lambda = lmbd

    def execute(self):
        self._lambda()
