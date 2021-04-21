"""
Event用来实现进程间同步通信。
感觉例子举的不好，没看出来哪里使用了进程间同步通讯
好像看明白了
但不太明白如果需要多个事件怎么命名？？
"""
import multiprocessing
import time

def wait_for_event(e, ):
    print("wait_for_event: starting")
    e.wait()  #e.wait在这儿又是什么作用？？等待事件e是否被set，空置说明一直等待事件e置位set
    print("wairt_for_event: e.is_set()->" + str(e.is_set()))  #这一句在主进程运行完毕后运行

def wait_for_event_timeout(e, t):
    print("wait_for_event_timeout:starting")
    e.wait(t)   #事件计时？？等待事件e是否被set，规定时间内没等到，则返回false
    print("wait_for_event_timeout:e.is_set->" + str(e.is_set()))#事件计时超出返回false？？

if __name__ == "__main__":
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(name = "block",
            target = wait_for_event,
            args = (e,))

    w2 = multiprocessing.Process(name = "non-block",
            target = wait_for_event_timeout,
            args = (e, 2))
    w1.start()
    w2.start()

    time.sleep(3)

    e.set()#这句语句又是什么意思？？事件e置位,在主进程执行完毕再次执行子进程时，子进程等待完毕
            #若没有这句语句，子进程一直等待，主进程执行完毕，程序仍然不结束，等待e事件置位
    print("main: event is set")