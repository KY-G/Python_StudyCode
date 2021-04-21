import multiprocessing as mp
from time import sleep
from random import randint
import os

def test():
    sleep(randint(0,4))
    print(os.getppid(),'-------',os.getpid())
    print("Testing")

if __name__ == '__main__':

    for i in range(5):
        p = mp.Process(target=test)  # 原test()函数已经不是普通的函数，Process对象已经将其转变成进程。
        p.start()
