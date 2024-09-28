from queue import Queue

from src.command import ICommand
from src.exception_handler import ExceptionHandler
from threading import Thread


class GameThreadLoop(ICommand):

    def __init__(self, exception_handler: ExceptionHandler):
        self.queue = Queue()
        self.exception = exception_handler
        self.thread = Thread(target=self._loop)
        self.stop = False
        self.behaviour_lambda = lambda: self.behaviour()

    def set_behaviour(self, behaviour):
        self.behaviour_lambda = behaviour

    def put_cmd(self, cmd: ICommand) -> None:
        self.queue.put(cmd)

    def behaviour(self):
        try:
            cmd = self.queue.get()
            print(f"Game loop. Run: {type(cmd)}")
            cmd.execute()
            print(f"Done: {type(cmd)}")
        except Exception as e:
            self.exception.handle(cmd, e)

    def hard_stop(self):
        self.stop = True

    def _loop(self):

        # TODO: before hook() - сделать что-то перед эвентлупом

        while not self.stop:
            try:
                self.behaviour_lambda()
            except Exception as _e:
                print(f"Log thread error: {_e}")

        # TODO: after hook() - сделать что-то после завершения, например, остаток очереди сохранить

    def execute(self) -> None:
        self.thread.start()
