from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from src.exception_handler import ExceptionHandler
from src.game_exceptions import MoveExceptions, ExceptionLog, ExceptionLogQueue, \
    RetryCmdNow, RetryCmdNowQueue
from src.game_loop import GameLoop, game_loop
from src.movement import IMovable, MovableObjectAdaptor, Vector, IUserObject, Move


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



class ExceptionTestCase(TestCase):

    def test_game_loop_successful(self):
        # Проверка game_loop
        exception = ExceptionHandler()
        exception.register_handler(Move, AttributeError, MoveExceptions)
        game = GameLoop(exception)

        obj = MockUserObject()
        obj.set_property("position", Vector([12.0, 5.0]))
        obj.set_property("velocity", Vector([-7, 3]))

        movable = MovableObjectAdaptor(obj)
        move = Move(movable)

        game.put_cmd(move)
        game.run()

        self.assertTrue(obj.get_property("position") == Vector([5, 8]))

    def test_exception_rise(self):
        # Проверка отработки исключения в game_loop
        exception = ExceptionHandler()
        exception.register_handler(Move, AttributeError, MoveExceptions)
        game = GameLoop(exception)

        obj = MockUserObject()
        obj.set_property("position", Vector([12.0, 5.0]))
        obj.set_property("velocity", Vector([-7, 3]))

        movable = MovableObjectAdaptor(obj)
        move = Move(movable)

        game.put_cmd(move)

        mock_movable = Mock(spec_set=IMovable)
        mock_movable.get_position.side_effect = NotImplementedError()
        except_move = Move(MovableObjectAdaptor(mock_movable))
        game.put_cmd(except_move)

        self.assertRaises(NotImplementedError, game.run)

    def test_exception_to_log(self):
        # Реализовать Команду, которая записывает информацию о выброшенном исключении в лог.
        exception = ExceptionHandler()
        exception.register_handler(Move, AttributeError, ExceptionLog)
        game = GameLoop(exception)

        mock_movable = Mock(spec_set=IMovable)
        mock_movable.get_position.side_effect = NotImplementedError()
        except_move = Move(MovableObjectAdaptor(mock_movable))
        game.put_cmd(except_move)

        game.run()

    def test_exception_queue_log(self):
        # Реализовать обработчик исключения, который ставит Команду, пишущую в лог в очередь Команд.
        game_loop.exception.reset_handler()
        game_loop.exception.register_handler(Move, AttributeError, ExceptionLogQueue)

        mock_movable = Mock(spec_set=IMovable)
        mock_movable.get_position.side_effect = NotImplementedError()
        except_move = Move(MovableObjectAdaptor(mock_movable))
        game_loop.put_cmd(except_move)

        game_loop.run()

    def test_exception_retry(self):
        # Реализовать Команду, которая повторяет Команду, выбросившую исключение.
        game_loop.exception.reset_handler()
        game_loop.exception.register_handler(Move, AttributeError, RetryCmdNow)

        mock_movable = Mock(spec_set=IMovable)
        mock_movable.get_position.side_effect = NotImplementedError()
        except_move = Move(MovableObjectAdaptor(mock_movable))
        game_loop.put_cmd(except_move)

        self.assertRaises(AttributeError, game_loop.run)

    def test_exception_retry_queue(self):
        # Реализовать обработчик исключения, который ставит в очередь Команду - повторитель команды, выбросившей исключение.
        game_loop.exception.reset_handler()
        game_loop.exception.register_handler(Move, AttributeError, RetryCmdNowQueue)

        mock_movable = Mock(spec_set=IMovable)
        mock_movable.get_position.side_effect = NotImplementedError()
        except_move = Move(MovableObjectAdaptor(mock_movable))
        game_loop.put_cmd(except_move)

        self.assertRaises(AttributeError, game_loop.run)

    def test_exception_first_retry_second_log(self):
        # С помощью Команд из пункта 4 и пункта 6 реализовать следующую обработку исключений:
        # при первом выбросе исключения повторить команду, при повторном выбросе исключения записать информацию в лог.
        game_loop.exception.reset_handler()
        game_loop.exception.register_handler(MockCmd, Exception, RetryCmdNowQueue)
        game_loop.exception.register_handler(RetryCmdNow, Exception, ExceptionLog)

        mock = MockCmd()
        game_loop.put_cmd(mock)

        game_loop.run()

        assert mock.count == 2






