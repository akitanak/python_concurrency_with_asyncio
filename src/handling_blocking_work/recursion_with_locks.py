from threading import Lock, Thread
from typing import List

list_lock = Lock()
list = [1, 2, 3, 4]


def sum_list(int_list: List[int]) -> int:
    print("Waiting to aquire lock.")
    # この処理ではsum_listを再帰的に呼び出している。
    # 呼び出し元で取得したlockを開放せずに
    # 再起呼び出しした同関数内でlockを再び取得しようとしているので、
    # lockは永遠に取得できず処理を進めることができなくなってしまう。
    with list_lock:
        print("Acquired lock.")
        if len(int_list) == 1:
            print("Finished summing.")
            return int_list[0]
        else:
            head, *tail = int_list
            print("Summing rest of list.")
            return head + sum_list(tail)


thread = Thread(target=sum_list, args=(list,))
thread.start()
thread.join()
