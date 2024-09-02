from src.command import ICommand
from collections import defaultdict


class ExceptionHandler:

    def __init__(self):
        self._store = defaultdict(dict)

    def handle(self, c: ICommand, e: Exception):
        self._store.get(type(c)).get(type(e))(c, e).execute()

    def register_handler(self, ct: ICommand, et: Exception, c: ICommand):
        self._store[ct][et] = c

    def reset_handler(self):
        self._store = defaultdict(dict)



