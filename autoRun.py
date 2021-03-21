import os
import subprocess
import sys

from time import sleep

log_file = "/home/lichendi/out.log"


def open0(command):
    import subprocess
    import sys
    with open(log_file, 'wb+') as f:  # replace 'w' with 'wb' for Python 3
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        for line in process.stdout:
            print("gogo")
            print(line)
        for c in iter(lambda: process.stdout.read(1), b''):  # replace '' with b'' for Python 3
            sys.stdout.write(c)
            f.write(str(c))
    return "writed to logfile: " + log_file

def open1(command):
    f = open(log_file, 'w+') 
    
    print("1")
    ret_val = subprocess.Popen(command, stdout=f, stderr=subprocess.PIPE, shell=True )
    print("2")
    while not ret_val.poll():
        print("3")
        f.flush()
    print("4")
    return "write to log_file: " + log_file

def open2(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    list = []
    for line in iter(proc.stdout.readline, ''):
        list.append(line)
        #print(line)  # process line-by-line
    return list

def subprocess_popen(statement):
    p = subprocess.Popen(statement, shell=True, stdout=subprocess.PIPE)  # 执行shell语句并定义输出格式
    while p.poll() is None:  # 判断进程是否结束（Popen.poll()用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码）
        if p.wait() is not 0:  # 判断是否执行成功（Popen.wait()等待子进程结束，并返回状态码；如果设置并且在timeout指定的秒数之后进程还没有结束，将会抛出一个TimeoutExpired异常。）
            print("command execute failed")
            return False
        else:
            re = p.stdout.readlines()  # 获取原始执行结果
            result = []
            for i in range(len(re)):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
                res = re[i].decode('utf-8').strip('\r\n')
                result.append(res)
            return result


def execAndPrint(command):
    r = os.popen(command) #执行该命令
    info = r.readlines()  #读取命令行的输出到一个list
    for line in info:  #按行遍历
        line = line.strip('\r\n')
    return info

# compile multi-threaded Fake_OpenBLAS
def compileFake():
    print("compiling Fake_OpenBLAS...")
    compileLog = os.system("cd /home/lichendi/git/Fake_OpenBLAS\n make -j FC=gfortran NO_LAPACK=1 USE_THREAD=1 DEBUG=1")
    return compileLog

# run BLAS-test
def runTest():
    print("running test...")
    result = open0('cd /home/lichendi/git/BLAS-test/build && cmake .. && make -j && make run')
    #result = open1("cd /home/lichendi/git/BLAS-test/build && cmake .. && make -j && make run")
    #result = open2("cd /home/lichendi/git/BLAS-test/build && cmake .. && make -j && make run")
    #result = execAndPrint("cd /home/lichendi/git/BLAS-test/build && cmake .. && make -j && make run")
    #result = subprocess_popen("cd /home/lichendi/git/BLAS-test/build && cmake .. && make -j && make run")
    #perf = os.system("cd /home/lichendi/git/BLAS-test/build && cmake .. && make -j && make run")
    return result

def modifyByConfig(config):
    print("###error: did't do modify!!!")

def autoTune(config):
    modifyByConfig(config)
    print("modify by config done!")
    print("sleeping")
    #sleep(3)
    #compileFake()
    info = runTest()
    return info