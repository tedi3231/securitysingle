#coding=utf8
#获取硬件信息

import os

def getMemoryInfo():
    """
    get memery infomation,include total,free,used and used percent
    """
    temp = os.popen('cat -A /proc/meminfo').read()
    lines = temp.split('$')    
    resultList = [line for line in lines if line.strip().startswith(('MemTotal','MemFree',))]    
    result ={}
    for k,v in  [(item.split()[0],int(item.split()[1])/1024) for item in resultList]:
        result[k.split(':')[0]] = v    
    result["MemUsed"] = result['MemTotal'] - result['MemFree']
    result["Percent"] = 100 -(float(result["MemUsed"])/result['MemTotal'])*100
    return result

def get_df_data(datapath):
    """
    get hard disk infomation, datapath is the path where you save data
    """
    cmd = "df -h -l -P %s" % datapath    
    pipe = os.popen(cmd)
    data = pipe.read().strip()    
    rows = []    
    lines =  data.split("\n")    
    header = rows.append( tuple(lines[0].split()) )    
    del lines[0]
    for line in  lines:
        rows.append(tuple(line.split()))
    return rows        

def get_time_info( ):
    """
    get system starttime and how long time that the system has run
    """
    startTimeCmd = "date -d \"$(awk -F. '{print $1}' /proc/uptime) second ago\" +\"%Y-%m-%d %H:%M:%S\""
    runTimeCmd = "cat /proc/uptime"
    runTimeSecond = float( os.popen(runTimeCmd).read().strip().split()[0] )
    runTimeText = str.format("{0}天{1}小时{2}分{3}秒",int(runTimeSecond/86400),int((runTimeSecond%86400)/3600),int((runTimeSecond%3600)/60),int(runTimeSecond%60) )
    return {'starttime':os.popen(startTimeCmd).read().strip(),'runtime':runTimeText}
    
def getNetworkInfo( ):
    temp = os.popen("ifconfig").read()
    print temp
            
if __name__ == "__main__":
    info = get_time_info()
    print info['runtime']    
    #print getMemoryInfo()    
    #print getNetworkInfo()
    """
    rows = get_df_data('/var')
    for row in rows:
        for col in row:
            print col
        print "\n"    
    """

