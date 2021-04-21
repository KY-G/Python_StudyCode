# coding:utf-8
import os
import datetime


time_now = datetime.datetime.now().strftime('%H:%M:%S.%f')
print(time_now)

out = os.system('c: && cd \Program Files (x86)\Tobii\Tobii Configuration && Tobii.Configuration.exe -Q') #加&&可执行多条语句
print(out)
time_now = datetime.datetime.now().strftime('%H:%M:%S.%f')
print(time_now)
##未知原因导致使用：time.clock()和time.time()获取的时间都是错的
#获取本地时间后可得校准加保存校准数据共用时17s

# path = "C:\Program Files (x86)\Tobii\Tobii Configuration"
# path_2 = '\Program Files (x86)\Tobii\Tobii Configuration'
# # 查看当前工作目录
# retval = os.getcwd()
# print("当前工作目录为 %s" % retval)
#
# # 修改当前工作目录
# os.chdir(path)
#
# # 查看修改后的工作目录
# retval = os.getcwd()
# print("目录修改成功 %s" % retval)

#os.startfile(r'C:\Program Files (x86)\Tobii\Tobii Configuration\Tobii.Configuration.exe')  #执行后，相当于双击文件

#os.popen("'C:\Program Files (x86)\Tobii\Tobii Configuration\Tobii.Configuration.exe' -Q")
#os.system("'cd \Program Files (x86)\Tobii\Tobii Configuration\Tobii.Configuration.exe' -Q")
#os.system("dir")#cmd起始文件在存放python程序的位置

# os.system('c:')
# print(os.system('c:'))
# os.system('dir')
# sleep(1)
# if(os.system('c:') == 0):
#     os.system("cd \Program Files (x86)")
#     print(os.system("cd \Program Files (x86)"))