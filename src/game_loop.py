from queue import Queue

from src.command import ICommand
from src.exception_handler import ExceptionHandler


class GameLoop:

    def __init__(self, exception_handler: ExceptionHandler):
        self.queue = Queue()
        self.exception = exception_handler

    def put_cmd(self, cmd: ICommand) -> None:
        self.queue.put(cmd)

    def run(self) -> None:
        while not self.queue.empty():
            try:
                cmd = self.queue.get()
                print(f"Game loop. Run: {type(cmd)}")
                cmd.execute()
                print(f"Done: {type(cmd)}")
            except Exception as e:
                self.exception.handle(cmd, e)


game_exception_handler = ExceptionHandler()
game_loop = GameLoop(game_exception_handler)
