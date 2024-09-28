from threading import Event
from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from src.adapter import AdapterMetaClass
from src.command import LambdaCommand
from src.exception_handler import ExceptionHandler
from src.game_exceptions import MoveExceptions, ExceptionLog, ExceptionLogQueue, \
    RetryCmdNow, RetryCmdNowQueue
from src.game_thread_loops import GameThreadLoop #, game_thread
from src.movement import IMovable, MovableObjectAdaptor, Vector, IUserObject, Move
from src.ioc import IoC


class MockUserObject(IUserObject):

    def __init__(self):
        self._properties = {}

    def get_property(self, key: str) -> Any:
        return self._properties[key]

    def set_property(self, key: str, value: str) -> None:
        self._properties[key] = value


class MockCmd:

    def __init__(self):
        self.count = 0

    def execute(self):
        self.count += 1
        raise Exception


class MockEventSet():

    def __init__(self, event):
        self._event = event

    def execute(self):
        self._event.set()


class ThreadTestCase(TestCase):

    def test_game_loop_hard_stop(self):
        exception = ExceptionHandler()
        exception.register_handler(Move, AttributeError, MoveExceptions)
        game = GameThreadLoop(exception)

        obj = MockUserObject()
        obj.set_property("position", Vector([12.0, 5.0]))
        obj.set_property("velocity", Vector([-7, 3]))

        IoC.resolve(
            'IoC.Register',
            'MovableAdapter',
            AdapterMetaClass,
        ).execute()

        movable_meta_adapter = IoC.resolve('MovableAdapter', IMovable).execute()
        movable = movable_meta_adapter(obj)

        move = Move(movable)

        game.put_cmd(move)
        event = Event()

        hard_stop_cmd = LambdaCommand(lambda: (game.hard_stop(), event.set()))
        game.put_cmd(hard_stop_cmd)
        # этот шаг не должен выполниться, перед ним хард стоп
        game.put_cmd(move)
        # game.put_cmd(MockEventSet(event))
        game.execute()

        event.wait()

        self.assertTrue(obj.get_property("position") == Vector([5, 8]))

    def test_game_loop_soft_stop(self):
        exception = ExceptionHandler()
        exception.register_handler(Move, AttributeError, MoveExceptions)
        game = GameThreadLoop(exception)

        obj = MockUserObject()
        obj.set_property("position", Vector([12.0, 5.0]))
        obj.set_property("velocity", Vector([-7, 3]))

        IoC.resolve(
            'IoC.Register',
            'MovableAdapter',
            AdapterMetaClass,
        ).execute()

        movable_meta_adapter = IoC.resolve('MovableAdapter', IMovable).execute()
        movable = movable_meta_adapter(obj)

        move = Move(movable)

        game.put_cmd(move)
        event = Event()

        soft_stop_cmd = LambdaCommand(
                lambda: game.set_behaviour(
                    lambda: game.hard_stop() if game.queue.empty() else game.behaviour()
                )
            )
        game.put_cmd(soft_stop_cmd)
        game.put_cmd(move)
        game.put_cmd(MockEventSet(event))
        game.execute()

        event.wait()
        self.assertTrue(obj.get_property("position") != Vector([5, 8]))


    def test_exception_rise(self):
        # Проверка отработки исключения в game_loop
        exception = ExceptionHandler()
        exception.register_handler(Move, AttributeError, MoveExceptions)
        game = GameThreadLoop(exception)

        mock_movable = Mock(spec_set=IMovable)
        mock_movable.get_position.side_effect = NotImplementedError()
        except_move = Move(MovableObjectAdaptor(mock_movable))
        game.put_cmd(except_move)
        game.execute()
        game.put_cmd(LambdaCommand(lambda: game.hard_stop()))
