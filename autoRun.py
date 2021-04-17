#coding=utf-8
import os
import subprocess
import sys

from time import sleep

log_file = "/home/lichendi/out.log"
packfile = "/home/lichendi/git/Fake_OpenBLAS/driver/level3/gemm_pack.c"
computefile = "/home/lichendi/git/Fake_OpenBLAS/driver/level3/gemm_compute.c"
#def open3(command):
#    procExe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#
#    while procExe.poll() is None:
#        line = procExe.stdout.readline()
#        #print("Print:" + line, flush = True)
#
#def open0(command):
#    import subprocess
#    import sys
#    with open(log_file, 'wb+') as f:  # replace 'w' with 'wb' for Python 3
#        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
#        for line in process.stdout:
#            print("gogo")
#            print(line)
#        for c in iter(lambda: process.stdout.read(1), b''):  # replace '' with b'' for Python 3
#            sys.stdout.write(c)
#            f.write(str(c))
#    return "writed to logfile: " + log_file
#
#def open1(command):
#    f = open(log_file, 'w+') 
#    
#    print("1")
#    ret_val = subprocess.Popen(command, stdout=f, stderr=subprocess.PIPE, shell=True )
#    print("2")
#    while not ret_val.poll():
#        print("3")
#        f.flush()
#    print("4")
#    return "write to log_file: " + log_file
#
#def open2(command):
#    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
#    list = []
#    for line in iter(proc.stdout.readline, ''):
#        list.append(line)
#        #print(line)  # process line-by-line
#    return list
#
#def subprocess_popen(statement):
#    p = subprocess.Popen(statement, shell=True, stdout=subprocess.PIPE)  # 执行shell语句并定义输出格式
#    while p.poll() is None:  # 判断进程是否结束（Popen.poll()用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码）
#        if p.wait() is not 0:  # 判断是否执行成功（Popen.wait()等待子进程结束，并返回状态码；如果设置并且在timeout指定的秒数之后进程还没有结束，将会抛出一个TimeoutExpired异常。）
#            print("command execute failed")
#            return False
#        else:
#            re = p.stdout.readlines()  # 获取原始执行结果
#            result = []
#            for i in range(len(re)):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
#                res = re[i].decode('utf-8').strip('\r\n')
#                result.append(res)
#            return result


def execAndPrint(command):
    r = os.popen(command) #执行该命令
    info = r.readlines()  #读取命令行的输出到一个list
    for line in info:  #按行遍历
        line = line.strip('\r\n')
    return info

# compile multi-threaded Fake_OpenBLAS
def compileFake():
    print("compiling Fake_OpenBLAS...")
    compileLog = os.system("cd /home/lichendi/git/Fake_OpenBLAS && make -j FC=gfortran NO_LAPACK=1 USE_THREAD=0")
    return compileLog

# run BLAS-test
def runTest(p, q, i):
    p = p + i * 8
    q = q + i * 8
    print("running test...")
    os.system("cd /home/lichendi/git/BLAS-test/build && make clear && cmake .. && make -j && make run")
    result = os.system("mv /home/lichendi/git/BLAS-test/output/out.txt /home/lichendi/git/BLAS-test/output/P"+str(p)+"Q"+str(q)+".txt")

    return result

def alter(file, old_str, new_str):
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = new_str
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)

def testACC(p, q, i):
    p = p + i * 8
    q = q + i * 8
    print("running ACC test...")
    os.system("cd /home/lichendi/git/ACC_BLAS/build && make clear && cmake .. && make -j && make run")
    result = os.system("mv /home/lichendi/git/ACC_BLAS/output/out.txt /home/lichendi/git/ACC_BLAS/output/P"+str(p)+"Q"+str(q)+".txt")
    return result

def modifyByConfig(p, q, i):
    p = p + i * 8
    q = q + i * 8
    alter(packfile, "define GEMM_P", "#define GEMM_P " + str(p) + "\n")
    alter(packfile, "define GEMM_Q", "#define GEMM_Q " + str(q) + "\n")
    alter(computefile, "define GEMM_P", "#define GEMM_P " + str(p) + "\n")
    alter(computefile, "define GEMM_Q", "#define GEMM_Q " + str(q) + "\n")
    #print("config :")
    #print(config)
    print("###error: did't do modify!!!")
    #exit()

def autoTune(p, q, i):
    modifyByConfig(p, q, i)
    print("modify by p, q, i done!")
    print("sleep 1s")
    sleep(1)

    if not compileFake():
        print("compile done!")
    print("sleep 1s")
    sleep(1)

    if not testACC(p, q, i):
        print("ACC test done!")
    print("sleep 1s")
    sleep(1)

    if not runTest(p, q, i):
        print("test done!")
        return "auto-tuning done!"
    else:
        return "auto-tuning fail!"