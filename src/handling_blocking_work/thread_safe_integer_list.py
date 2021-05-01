from threading import RLock
from typing import List


class IntListThreadsafe:
    lock = RLock()

    def __init__(self, wrapped_list: List[int]):
        self.inner_list = wrapped_list

    def indices_of(self, to_find: int) -> List[int]:
        print("Acquiring lock in indices_of.")
        with self.lock:
            enumerator = enumerate(self.inner_list)
            return [index for index, value in enumerator if value == to_find]

    def find_and_replace(self, to_replace: int, replace_with: int) -> None:
        print("Acquiring lock in find_and_replace.")
        with self.lock:
            indices = self.indices_of(to_replace)
            for index in indices:
                self.inner_list[index] = replace_with


threadsafe_list = IntListThreadsafe([1, 2, 1, 2, 1])
threadsafe_list.find_and_replace(1, 2)
print(threadsafe_list.inner_list)
