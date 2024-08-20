import logging

from src.command import ICommand
from src.game_loop import game_loop


class MoveExceptions:

    def __init__(self, cmd, e):
        raise NotImplementedError


class MoveExceptionsLog:

    def __init__(self, cmd, e):
        self.cmd = cmd
        self.e = e

    def execute(self):
        logging.log(logging.ERROR, f"Все сломалось. {type(self.cmd)}" f"{type(self.e)}")


class MoveExceptionsLogQueue:

    def __init__(self, cmd, e):
        self.cmd = cmd
        self.e = e

    def execute(self):
        ExceptionGameQueue(MoveExceptionsLog(self.cmd, self.e)).execute()


class ExceptionGameQueue:

    def __init__(self, cmd: ICommand):
        self.cmd = cmd

    def execute(self):
        game_loop.put_cmd(self.cmd)


class RetryCmdNow:

    def __init__(self, cmd, e):
        self.cmd = cmd
        self.e = e

    def execute(self):
        print(f"Нагло повторяем команду {type(self.cmd)} из RetryCmdNow")
        self.cmd.execute()


class RetryCmdNowQueue:

    def __init__(self, cmd, e):
        self.cmd = cmd
        self.e = e

    def execute(self):
        ExceptionGameQueue(RetryCmdNow(self.cmd, self.e)).execute()


class RetryCmd:

    def __init__(self, cmd, e):
        self.cmd = cmd
        self.e = e

    def execute(self):
        return self.cmd


class RetryCmdQueue:

    def __init__(self, cmd, e):
        self.cmd = cmd
        self.e = e

    def execute(self):
        ExceptionGameQueue(RetryCmd(self.cmd, self.e)).execute()
