"""
主要涉及Semaphore的使用，用来控制对共享资源的访问数量，例如池的最大连接数。
不太明白，慢慢研究
"""
import multiprocessing
import time

def worker(s, i):
    s.acquire()
    print(multiprocessing.current_process().name + "acquire")
    time.sleep(i)
    print(multiprocessing.current_process().name + "release\n")
    s.release()

if __name__ == "__main__":
    s = multiprocessing.Semaphore(2)
    for i in range(5):
        p = multiprocessing.Process(target = worker, args=(s, i*2))
        p.start()