from src.ioc import IoC
import inspect

class AdapterMetaClass:

    def __init__(self, interface):

        def init(self, obj):
            self._obj = obj
            IoC.resolve(
                "IoC.Register",
                'IMovable.position.get',
                lambda: self._obj.get_property("position")
            ).execute()

            IoC.resolve(
                "IoC.Register",
                'IMovable.velocity.get',
                lambda: self._obj.get_property("velocity")
            ).execute()

            IoC.resolve(
                "IoC.Register",
                'IMovable.position.set',
                lambda vector: self._obj.set_property("position", vector)
            ).execute()

            IoC.resolve(
                "IoC.Register",
                'IMovable.velosity.set',
                lambda vector: self._obj.set_property("position", int)
            ).execute()

        def getter(self):
            method_name = inspect.currentframe().f_code.co_name
            self._print_method_name()
            return IoC.resolve(
                f'IMovable.{method_name.split("_")[1]}.get'
            )

        def setter(self, value):
            self._obj = value

        meta_methods = {
            '__init__': init,
            '_print_method_name': lambda self: print(
                f"Метод: {inspect.currentframe().f_back.f_code.co_name}",
                print(inspect.currentframe().f_code.co_name),
            )
        }
        prop = []
        # разбор интерфейса
        for key, val in interface.__dict__.items():
            if key[0] != '_':
                if key.split('_')[0] == 'get':
                    # meta_methods[key] = getter
                    prop = f'IMovable.{key.split("_")[1]}.get'
                    meta_methods[key] = lambda self, prop=prop: \
                        IoC.resolve(
                            prop
                        )
                if key.split('_')[0] == 'set':
                    meta_methods[key] = setter
                    prop = f'IMovable.{key.split("_")[1]}.set'
                    meta_methods[key] = lambda self, vector, prop=prop: \
                        IoC.resolve(
                            prop, vector
                        )

        # создание класса адаптера
        M = type(f"MetaAdaptor{interface.__name__}", (), meta_methods)
        self._M = M

    def execute(self):
        return self._M
