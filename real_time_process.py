"""
主要涉及到电脑实时时间的语句,以及主子程序运行顺序问题。
"""

import multiprocessing
import time
import os

def worker(interval):
    n = 5
    while n > 0:
        print("The time is {0}".format(time.ctime()))#输出实时的时间
        time.sleep(interval)
        n -= 1

# class MyProcess(multiprocessing.Process():
#     def worker(interval):
#         n = 5
#         while n > 0:
#             print("The time is {0}".format(time.ctime()))  # 输出实时的时间
#             time.sleep(interval)
#             n -= 1
#     def __del__(self):
#         print("删除成功！")
"""
这种方式尚且不知道如何将参数传进去，不能直接就运行删除程序啊
"""

if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (3,))
#    p = MyProcess(args = (3,))
    p.start()   #这里明明先开始的子程序，为什么主程序运行完才开始子程序？？
#    p.join()  # 主进程阻塞等待子进程的退出，加上这段语句就会先运行子程序再运行主程序
    print("p.pid:", p.pid)
    print ("p.name:", p.name)
    print ("p.is_alive:", p.is_alive())
    print("The number of CPU is:" + str(multiprocessing.cpu_count()))