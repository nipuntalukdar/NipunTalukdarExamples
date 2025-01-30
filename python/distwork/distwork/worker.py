import secrets
from .dumpload import DumpLoad
from .redis_stream import RedisStream


class Worker:
    def __init__(
        self,
        redis_url: str = "redis://127.0.0.1:6379",
        task_stream: str = "tasks",
        task_group: str = "taskgroup",
    ):
        self._redis_url = redis_url
        self._task_stream = task_stream
        self._task_group = task_group
        self._redis_stream = RedisStream(redis_url, task_stream, task_group)

    def __call__(self, work_func, *args, **kwargs):
        try:
            return_data = work_func(*args, **kwargs)
            return return_data, "OK"
        except:
            return False, "NOTOK"

    def do_work(self, consumer_id: str | None = None):
        my_id = consumer_id
        if not consumer_id:
            my_id = f"worker_{secrets.token_hex()}"

        while True:
            print("Getting work")
            self._redis_stream.dequeue_work(self, my_id)
