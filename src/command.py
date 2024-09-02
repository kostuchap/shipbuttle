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