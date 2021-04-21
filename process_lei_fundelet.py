"""
主要涉及到将进程定义为类，如何传入在类中传入函数的参数
类子进程的执行顺序
进程删除原理。
进程p调用start()时，自动调用run()
"""
import multiprocessing
import time

class ClockProcess(multiprocessing.Process):
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval
        print("进程初始化")

    def run(self):
        n = 3
        while n > 0:
            print("the time is {0}".format(time.ctime()))
            time.sleep(self.interval)
            n -= 1

    def __del__(self):  #只要调用了这个，在主程序运行结束，必定会再次输出一次销毁子程序
        print("删除成功！")

if __name__ == '__main__':
    p = ClockProcess(1)
    p.start()
    p.join()
    print("主程序运行完成")