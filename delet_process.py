"""
当重写Process的run方法创建进程后，可以看到windows系统会在子进程执行完毕后立即删除Process对象，
同时在主进程结束后，windows系统会将主进程的Process对象删除，也就是会出现两次“删除成功”，
一个进程删除一次，如果只创建一个子进程就会出现一次删除成功

"""

import multiprocessing as ms
import time
import os

class MyProcess(ms.Process):
    def run(self):
        print("这是进程！", os.getpid())

    def __del__(self):
        print("删除成功！")


def main():
    p1 = MyProcess()
    p2 = MyProcess()
    p1.start()
    time.sleep(1)
    p2.start()
    time.sleep(1)
    p2.join()  #等待进程结束
    print("主进程结束")
    # print(ms.active_children())
    # while True:
    #     time.sleep(0.01)
if __name__ == "__main__":
    main()