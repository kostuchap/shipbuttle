from queue import Queue

from src.command import ICommand
from src.exception_handler import ExceptionHandler
from threading import Thread


class GameThreadLoop:

    def __init__(self, exception_handler: ExceptionHandler):
        self.queue = Queue()
        self.exception = exception_handler
        self.thread = Thread(target=self._loop)

    def put_cmd(self, cmd: ICommand) -> None:
        self.queue.put(cmd)

    def _loop(self):
        while not self.queue.empty():
            try:
                cmd = self.queue.get()
                print(f"Game loop. Run: {type(cmd)}")
                cmd.execute()
                print(f"Done: {type(cmd)}")
            except Exception as e:
                self.exception.handle(cmd, e)

    def run(self) -> None:
        self.thread.start()


game_exception_handler = ExceptionHandler()
game_thread = GameThreadLoop(game_exception_handler)
