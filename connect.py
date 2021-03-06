# coding: utf-8

import paramiko
import re
from time import sleep
import getpass
import time
import os
import socket
from os import path
logFile = '/usr/log.txt'
# 定义一个类，表示一台远端linux主机
class Linux(object):

    # 通过IP, 用户名，密码，超时时间,初始化一个远程Linux主机
    def __init__(self, ip, username, password, timeout=30):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout
        # transport和chanel
        self.t = ''
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 3

    # 调用该方法连接远程主机
    def connect(self):
        while True:
            # 连接过程中可能会抛出异常，比如网络不通、链接超时
            try:
                self.t = paramiko.Transport(sock=(self.ip, 22))
                self.t.connect(username=self.username, password=self.password)
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                # 如果没有抛出异常说明连接成功，直接返回
                print(u'连接%s成功' % self.ip)
                # 接收到的网络数据解码为str
                print(self.chan.recv(65535).decode('utf-8'))
                return
            # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
            except Exception as e1:
                if self.try_times != 0:
                    print(u'连接%s失败，进行重试' % self.ip)
                    self.try_times -= 1
                else:
                    print(u'重试3次失败，结束程序')
                    exit(1)

    # 断开连接
    def close(self):
        self.chan.close()
        self.t.close()

    # 发送要执行的命令
    def send(self, cmd):
        cmd += '\r'
        # 通过命令执行提示符来判断命令是否执行完成
        p = re.compile(r']#|]$')
        result = ''
        # 发送要执行的命令
        self.chan.send(cmd)

        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        while True:
            sleep(2)
            ret = self.chan.recv(65535)
            ret = ret.decode('utf-8')
            result += ret
            if p.search(ret):
                return (result)
'''

def getExcuteInfo():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]

     
            f = open(logFile, 'a+')
            f.write('操作IP:' + ip + '执行时间:' + time.ctime())
            f.close()
        else:
            f = open(logFile,'a+')
            f.write('操作IP:'+ip+'执行时间:'+time.ctime())
            f.close()
        
        if not os.path.exists(log):
            os.system(r'touch {}'.format(log))
            print('新建成功')
            f = open(log,'w')
            f.write('操作IP:'+ip+'执行时间:'+time.ctime())
            f.close()
       
        else:
            with open(log,'a+') as f:
                f.write('操作IP:' + ip + '执行时间:' + time.ctime())
                print('追加成功')
            #f.close()
        
    finally:
        s.close()
    return ip

def uploadFiles():
    if path.exists(logFile):
        print('文件已经存在')
    else:
        print('文件不存在！')
        with open('C:\\Users\\Rain Sunny\\Desktop\\log.txt','a+') as f:
            f.write('操作IP:' + getExcuteInfo() + '执行时间:' + time.ctime())

'''

if __name__ == '__main__':
    #host_ip = input("请输入主机ip:\n")
    #pwd = getpass.getpass("请输入密码:\n")
    host_ip='121.4.86.9'
    pwd = 'Fyx123...'

    host = Linux(host_ip, 'root', pwd)

    host.connect()
   # host.send('cd /home;sh dbstop.sh;sh dbstart.sh')
    host.send('pwd')
    host.close()
    #getExcuteInfo()