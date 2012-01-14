#coding=utf8
#获取硬件信息

import os

def getMemoryInfo( ):
    outstream = os.popen('cat /proc/meminfo')
    print outstream.readline()
    print outstream.readline()
    print outstream.readline()

if __name__ == "__main__":    
    getMemoryInfo()


