from typing import Callable
import cloudpickle


class DumpLoad:
    @classmethod
    def dumpfn(cls, func: Callable, /, *args, **kwargs):
        dump_dict = {"func": func}
        if args:
            dump_dict["args"] = args
        if kwargs:
            dump_dict["kwargs"] = kwargs
        try:
            return cloudpickle.dumps(dump_dict)
        except Exception as e:
            return None

    @classmethod
    def loadfn(cls, data: str):
        try:
            dump_dict = cloudpickle.loads(data)
            print(dump_dict)
            return (
                dump_dict.get("func", None),
                dump_dict.get("args", ()),
                dump_dict.get("kwargs", {}),
            )
        except Exception as e:
            print(e)
            return None, None, None

    @classmethod
    def dump(cls, data):
        return cloudpickle.dumps(data)

    @classmethod
    def load(cls, data):
        return cloudpickle.loads(data)


if __name__ == "__main__":
    data = DumpLoad.dumpfn(lambda x, y: print(x, y), 1, 2)
    fun, args, kwargs = DumpLoad.loadfn(data)
    if not fun:
        exit(1)
    fun(*args, **kwargs)
