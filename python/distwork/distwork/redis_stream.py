from typing import Callable
import redis
from redis.exceptions import ResponseError

from .dumpload import DumpLoad


class RedisStream:
    def __init__(
        self,
        redis_url="redis://127.0.0.1:6379",
        task_stream="tasks",
        task_group="taskgroup",
        maxlen=1000000,
    ):
        self._redis_url = redis_url
        self._task_stream = task_stream
        self._task_group = task_group
        self._maxlen = maxlen
        self._redis = redis.StrictRedis.from_url(redis_url)
        try:
            self._redis.xgroup_create(task_stream, task_group, mkstream=True)
        except ResponseError as e:
            if str(e) != "BUSYGROUP Consumer Group name already exists":
                print(e)
                exit(1)
        except Exception as e:
            print(e)
            exit(1)

    def set(self, key: str, value: str):
        return self._redis.set(key, value)

    def create_stream(self, key: str, group: str, expiry: int = 86400):
        try:
            with self._redis.pipeline() as pipe:
                pipe.xgroup_create(key, group, mkstream=True)
                pipe.expire(key, expiry)
                pipe.execute()
        except ResponseError as e:
            if "BUSYGROUP Consumer Group name already exists" not in str(e):
                print(e)
                exit(1)
        except Exception as e:
            print(e)
            exit(1)

    def del_stream_group(self, key: str, group: str) -> bool:
        try:
            with self._redis.pipeline() as pipe:
                pipe.xgroup_destroy(key, group)
                pipe.delete(key)
                pipe.execute()
            return True
        except Exception as e:
            print(e)
            return False

    def enqueue_work(self, work: dict, stream: str = None) -> bool:
        the_stream = stream
        if not the_stream:
            the_stream = self._task_stream
        try:
            self._redis.xadd(the_stream, work)
            return True
        except Exception as e:
            print(e)
            return False

    def dequeue_work(self, worker_func: Callable, consumer_id: str, max_work: int = 5):
        works = self._redis.xreadgroup(
            self._task_group, consumer_id, {self._task_stream: ">"}, max_work, 10000
        )
        if not works:
            return True
        for stream, messages in works:
            for message in messages:
                message_id, message_data = message
                if not message_data or b"work" not in message_data:
                    self._redis.xack(self._task_stream, self._task_group, message_id)
                    continue
                func, args, kwargs = DumpLoad.loadfn(message_data[b"work"])
                if not func:
                    self._redis.xack(self._task_stream, self._task_group, message_id)
                    continue
                ret, ok = worker_func(func, *args, **kwargs)
                if ok == "OK":
                    if (
                        b"replystream" in message_data
                        and self.enqueue_work(
                            {"response": DumpLoad.dump(ret)},
                            message_data[b"replystream"],
                        )
                        or b"replystream" not in message_data
                    ):
                        self._redis.xack(
                            self._task_stream, self._task_group, message_id
                        )
                else:
                    print("Worker failed", message_id)
        return True

    def dequeue_response(
        self,
        stream: str,
        consumer_id: str,
        consumer_group: str,
        max_response: int = 100,
        max_wait=1000,
    ):
        responses = self._redis.xreadgroup(
            consumer_group, consumer_id, {stream: ">"}, max_wait, max_response, True
        )
        if not responses:
            return True
        for stream, messages in responses:
            for message in messages:
                message_id, message_data = message
                if not message_data or b"response" not in message_data:
                    continue
                response = DumpLoad.load(message_data[b"response"])
                print("Response", response)

    def trim(self):
        try:
            self._redis.xtrim(self._task_stream, self._maxlen)
        except Exception as e:
            print(e)

    def get(self, key) -> str:
        return self._redis.get(key)


if __name__ == "__main__":
    a = RedisStream(maxlen=200000)
    for i in range(10):
        a.enqueue_work({"a": i, "b": i * 2})
    a.dequeue_work()
    a.trim()
