#coding=utf8
#from griddata import Column
import datetime
import time
from schema import Column
import const
import os
import copy

author_list =  {'rows':[{'name':'  ', 'id':' '}, {'name':'tedi3231', 'id':'2'}], 'valuetext':'name', 'valuename':'id'}
dnstypelist = {'rows':[{'name':'白域名', 'id':'1'}, {'name':'恶意域名', 'id':'2'}, {'name':'动态域名', 'id':'3'}], 'valuetext':'name', 'valuename':'id'}
yesnolist =    {'rows':[{'name':'是','id':'1'},{'name':'否','id':'0'}],'valuetext':'name','valuename':'id'}
modulelist =    {'rows':[{'name':'参数管理','id':'systemparam'},{'name':'报警信息','id':'alarminfo'},{'name':'警报分析','id':'alarmanalysys'},{'name':'系统管理','id':'systemmanager'},{'name':'系统状态','id':'systemstatus'}],'valuetext':'name','valuename':'id'}

def moduleFormat(val):
    temp = [item for item in modulelist["rows"] if item["id"]==val]
    return (temp and len(temp)>0) and temp[0]["name"] or "没有找到对应模块"

def yesnoFormat( val ):
    if str(val) =='1':
        return '是'
    return '否'

def dnstypeformat(dnstype):
    temp = [item['name']  for item in dnstypelist['rows'] if str(item['id']) == str(dnstype)]
    if temp:
        return temp[0]
    return ''

def convertIpToInt(ipstr):
    """
    convert ip string to int 
    """
    vals = [int(item) for item in ipstr.split(".")]
    return vals[0] * 16777216 + vals[1] * 65536 + vals[2] * 256 + vals[3] * 1    

def convertIntToIp(val):
    """
    convert int value to string (ip)
    """
    vals = []
    vals.append(val / 16777216)
    val = val % 16777216
    vals.append(val / 65536)
    val = val % 65536
    vals.append(val / 256)
    val = val % 256
    vals.append(val)
    return ".".join([str(item) for item in vals])

def convertIntToDateStr(val):
    """
    convert int value to datetime string 
    """
    d1 = datetime.datetime.fromtimestamp(val)
    return d1.strftime("%Y-%m-%d %H:%M:%S")

def convertDateStrToInt(val):
    """
    covnert datetime string to int value
    """
    d1 = datetime.datetime.strptime(val,"%Y-%m-%d %H:%M:%S")    
    return  (int)(time.mktime(d1.timetuple()))

def generateMd5(val):
    import md5
    return md5.md5(val).hexdigest()

def restartSnort():
    """
    restart snort services
    """
    print "restart services"
    os.popen("service abc restart")

"""
dnslist
"""
const.DNSLIST_COLUMNS = (
    Column('id', 'id', controltype='hidden', show=False),
    Column('dnsname', '域名'),
    Column('type', '类型', control="select", formatter=dnstypeformat, controltype='select', easyclass='easyui-combobox', source=dnstypelist),
    Column('describ', '描述'),
)

const.DNSLIST_SEARCH = (
    {'name':'dnsname', 'title':'域名', 'validType':'', 'operation':'='},
)        

"""
EVILIP_LIST
"""
const.EVILIPLIST_COLUMNS = (
    Column('id', 'id', controltype='hidden', show=False),
    Column('startip', '开始地址', formatter=convertIntToIp, saveformatter=convertIpToInt, easyclass="easyui-validatebox", required="true"),
    Column('endip', '结束地址', formatter=convertIntToIp, saveformatter=convertIpToInt, easyclass="easyui-validatebox", required="true"),
    Column('describ', '描述'),
)

const.EVILIPLIST_SEARCH = (
    {'name':'startip', 'title':'开始地址', 'validType':'', 'operation':'='},
)


"""
TRO_DNS
"""
const.TRODNS_COLUMNS = (
    Column('id', 'id', controltype='hidden', show=False),
    Column('dnsname', '使用过的域名'),
    Column('describ', '描述'),
)

const.TRODNS_SEARCH = (
    {'name':'dnsname', 'title':'使用过的域名', 'validType':'', 'operation':'='},
)

"""
TRO_IP
"""
const.TROIP_COLUMNS = (
    Column('id', '木马号', controltype='hidden', show=False),
    Column('ip_addr', 'IP地址', formatter=convertIntToIp, saveformatter=convertIpToInt,easyclass="easyui-validatebox", required="true"),
    Column('time', '使用时间',formatter=convertIntToDateStr, saveformatter=convertDateStrToInt, easyclass="easyui-datebox", required="true"),
    Column('describ', '描述'),
)

const.TROIP_SEARCH = (
    {'name':'ip_addr', 'title':'IP地址', 'validType':'', 'operation':'='},
)

"""
GLOBALPARA
"""
const.GLOBALPARA_COLUMNS = (
    Column('id', 'id', controltype='hidden', show=False),
    Column('beaterror', '心跳偏差'),
    Column('beatcount', '心跳次数', defaultvalue=5),
    Column('dnsttl', '域名生存期', defaultvalue=60),
    Column('tcplasted', 'TCP长链接时间', defaultvalue=60),
    Column('tcpdivide', 'TCP链接内比值', defaultvalue=5),
    Column('tcpcount', 'TCP链接内次数', defaultvalue=5000),
    Column('httpsenddivide', 'HTTP发收比值', defaultvalue=5),
    Column('httppostdivide', 'HTTPPostGet比值', defaultvalue=5),
    Column('describ', '描述'),
)

const.GLOBALPARA_SEARCH = (
   {'name':'beaterror', 'title':'心跳偏差', 'validType':'', 'operation':'='},
)

"""
木马规则配置
"""
const.USER_TROJAN_RULE_COLUMNS = (
    Column('id', 'id', controltype='hidden', show=False),
    Column('srcip', '木马发起地址', formatter=convertIntToIp, saveformatter=convertIpToInt),
    Column('sport', '木马发起端口'),
    Column('dstip', '木马接收地址', formatter=convertIntToIp, saveformatter=convertIpToInt),
    Column('dport', '木马接收端口'),
    Column('offset', '特征串偏移量'),
    Column('dept', '特征串检测长度'),
    Column('proto', '协议'),
    Column('signature', '木马特征串'),
    Column('troname', '木马名称'),
    Column('isuser', '是否是用户自添加', controltype='hidden', show=False, defaultvalue='1'),
    Column('special', '控制被控端'),
    Column('desrib', '木马描述'),
)

const.USER_TROJAN_RULE_SEARCH = (
   {'name':'srcip', 'title':'木马发起地址', 'validType':'', 'operation':'='},
   {'name':'sport', 'title':'木马发起端口', 'validType':'', 'operation':'='},
   {'name':'dstip', 'title':'木马接收地址', 'validType':'', 'operation':'='},
   {'name':'dport', 'title':'木马接收端口', 'validType':'', 'operation':'='},
)


"""
ALARM
"""
const.ALARM_COLUMNS = (
    Column('id', 'id', controltype='hidden', show=False),
    Column('rid', 'rid', controltype='hidden', show=False, defaultvalue=0),
    Column('type', '报警类别'),
    Column('class', '报警级别'),
    Column('trojanid', '木马号'),
    Column('dip', '被控主机地址', formatter=convertIntToIp, saveformatter=convertIpToInt),
    Column('dmac', '被控主机MAC地址'),
    Column('sip', '控制主机地址', formatter=convertIntToIp, saveformatter=convertIpToInt),
    Column('scc', '控制主机所在国家'),
    Column('time', '报警时间',formatter=convertIntToDateStr),
    Column('alarm_msg', '报警描述'),
)

const.ALARM_SEARCH = (
   {'name':'type', 'title':'报警类别', 'validType':'', 'operation':'='},
)

"""
EVENT
"""
const.EVENT_COLUMNS = (
    Column('id', 'id', controltype='hidden', show=False),
    Column('pid', '事件规则集号', controltype='hidden', show=False, defaultvalue=0),
    Column('psid', '事件规则号', controltype='hidden', show=False, defaultvalue=0),
    #Column('time', '产生事件时间'),
    Column("countnum","事件产生个数"),
    Column('risk', '事件危险值'),
    Column('sip', '外部主机地址', formatter=convertIntToIp, saveformatter=convertIpToInt),
    Column('sport', '外部主机端口'),
    Column('dip', '内部主机地址', formatter=convertIntToIp, saveformatter=convertIpToInt),
    Column('dmac', '内部主机MAC地址'),
    Column('dport', '内部主机端口'),
    Column('pro', '协议'),
    Column('sflag', '是否包含域名', controltype='hidden', show=False, defaultvalue=0),
    Column('extradata', '事件描述'),
    Column('dns_name', '事件相关的域名', controltype='hidden', show=False, defaultvalue=''),
)

const.EVENT_SEARCH = (
   {'name':'type', 'title':'报警类别', 'validType':'', 'operation':'='},
)

"""
USERS
"""
const.USERS_COLUMNS = (
    Column('id', '编号', controltype='hidden', show=False),
    Column('username', '用户名'),
    Column('userpass', '密码',controltype="password",saveformatter=generateMd5,show=False),
    Column('remark', '备注'),
    #Column('permission', '权限'),
    Column('createdtime', '使用时间',formatter=convertIntToDateStr, saveformatter=convertDateStrToInt, controltype="hidden",defaultvalue=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),    
)

const.USERS_SEARCH = (
    {'name':'username', 'title':'用户名', 'validType':'', 'operation':'='},
)

"""
资源
"""
const.RESOURCES_COLUMNS = (
    Column('id', '编号', controltype='hidden', show=False),
    Column('module', '模块', control="select", controltype='select', formatter=moduleFormat, easyclass='easyui-combobox', source=modulelist),
    Column('title', '标题'),
    Column('controller', 'Controller'),
    Column('action', 'Action',defaultvalue=''),
    Column('isNav', '是否为菜单项',formatter = yesnoFormat, control="select", controltype='select', easyclass='easyui-combobox', source=yesnolist),
    Column('sortnum', '排序'),
    Column('createdtime', '创建时间',formatter=convertIntToDateStr, saveformatter=convertDateStrToInt, controltype="hidden",defaultvalue=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),    
)

const.RESOURCES_SEARCH = (
    {'name':'Controller', 'title':'Controller', 'validType':'', 'operation':'='},
    {'name':'Action', 'title':'Action', 'validType':'', 'operation':'='},
    {'name':'Module', 'title':'模块', 'validType':'', 'operation':'='},
)

"""
权限
"""
const.PERMISION_COLUMNS = (
    Column('id', '编号', controltype='hidden', show=False),
    Column('userid', '用户编号', controltype='hidden', show=False),
    Column('resourceid', '资源编号', controltype='hidden', show=False),
    Column('username', '用户名'),
    Column('module', '模块', control="select", controltype='select', formatter=moduleFormat, easyclass='easyui-combobox', source=modulelist),
    Column('title', '标题'),
    Column('controller', 'Controller'),
)

const.PERMISION_SEARCH = (
    {'name':'username', 'title':'用户名称', 'validType':'', 'operation':'='},  
)

"""
真正的权限表
"""
const.USERS_RESOURCES_COLUMNS = (
    Column('id', '编号', controltype='hidden', show=False),
    Column('userid', '用户编号', controltype='hidden', show=False),
    Column('resourceid', '资源编号', controltype='hidden', show=False),  
)

const.USERS_RESOURCES_SEARCH = (
    {'name':'id', 'title':'id', 'validType':'', 'operation':'='},  
)

const.LOGINFO_COLUMNS = (
    Column('id', 'id', controltype='hidden', show=False),
    Column('content', '内容',width=1000),
    Column('createdtime', '创建时间',show=False),    
)

const.LOGINFO_SEARCH = (
    {'name':'content', 'title':'内容', 'validType':'', 'operation':'like'},
)

const.entities = {
    "dnslist":{"tablename":"DNS_LIST", "columns":const.DNSLIST_COLUMNS, "search":const.DNSLIST_SEARCH},
    "evilip":{"tablename":"EVILIP_LIST", "columns":const.EVILIPLIST_COLUMNS, "search":const.EVILIPLIST_SEARCH},
    "trodns":{"tablename":"TRO_DNS", "columns":const.TRODNS_COLUMNS, "search":const.TRODNS_SEARCH},
    "troip": {"tablename":"TRO_IP", "columns":const.TROIP_COLUMNS, "search":const.TROIP_SEARCH},
    "globalpara": {"tablename":"GLOBALPARA", "columns":const.GLOBALPARA_COLUMNS, "search":const.GLOBALPARA_SEARCH,"aftersave":restartSnort},
    "alarm": {"tablename":"ALARM", "columns":const.ALARM_COLUMNS, "search":const.ALARM_SEARCH},
    "event": {"tablename":"EVENT", "columns":const.EVENT_COLUMNS, "search":const.EVENT_SEARCH},
    "usertrojanrule": {"tablename":"USER_TROJAN_RULE", "columns":const.USER_TROJAN_RULE_COLUMNS, "search":const.USER_TROJAN_RULE_SEARCH},
    "users": {"tablename":"USERS", "columns":const.USERS_COLUMNS, "search":const.USERS_SEARCH},
    "resources": {"tablename":"RESOURCES", "columns":const.RESOURCES_COLUMNS, "search":const.RESOURCES_SEARCH},
    "permision": {"tablename":"PERMISION_VIEW", "columns":const.PERMISION_COLUMNS, "search":const.PERMISION_SEARCH},
    "users_resources": {"tablename":"USERS_RESOURCES", "columns":const.USERS_RESOURCES_COLUMNS, "search":const.USERS_RESOURCES_SEARCH},
    "loginfo": {"tablename":"LOGINFO", "columns":const.LOGINFO_COLUMNS, "search":const.LOGINFO_SEARCH}
}
const.entities["alarm_1"] = copy.copy(const.entities["alarm"])
const.entities["event_1"] = copy.copy(const.entities["event"])
