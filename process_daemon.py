"""
主要涉及到p.daemon的使用
"""
import multiprocessing
import time

def worker(interval):
    print("work start:{0}".format(time.ctime()))
    time.sleep(interval)
    print("work end:{0}".format(time.ctime()))

if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (3,))
    p.daemon = True#加上这句后，随着主程序的结束，整个程序也就结束了，不会等待子程序执行。
    p.start()
    p.join()#加上这条语句，让子程序先于主程序执行完
    print("end!")