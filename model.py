#from griddata import Column
#coding=utf8
from schema import Column
import const

author_list = {'rows':[{'name':'  ','id':' '},{'name':'tedi3231','id':'2'}],'valuetext':'name','valuename':'id'}
dnstypelist = {'rows':[{'name':'白域名','id':'1'},{'name':'恶意域名','id':'2'},{'name':'动态域名','id':'3'}],'valuetext':'name','valuename':'id'}

def dnstypeformat( dnstype ):
    temp =[item['name']  for item in dnstypelist['rows'] if str(item['id'])==str(dnstype)]
    if temp:
        return temp[0]
    return ''

'''
Authors table's columns
'''
const.AUTHOR_COLUMNS = [
            Column('name', 'First Name' ),
            Column('email', 'Email'),
            Column('id', 'ID',controltype="hidden",show=False)
           ]

const.AUTHOR_SEARCH = (
    {"name":"name","title":"Name","validType":"","operation":"like"},
    {"name":"email","title":"Email","validType":"email","operation":"="},    
)
'''
Entries table's columns 
'''
const.ENTRIES_COLUMNS = (
            Column('slug', 'Slug'),
            Column('title', 'title'),
            Column('markdown', 'markdown', ),
            Column('html', 'html'), 
            Column('published', 'published',easyclass="easyui-datebox"),
            Column('updated', 'updated',easyclass="easyui-datebox"),
            Column('author_id', 'author_id',controltype="select",source=author_list),
            Column('id', 'id', controltype='hidden',show=False),
           )

const.ENTRIES_SEARCH = (
    {"name":"slug","title":"slug","validType":"","operation":"="},
    {"name":"title","title":"Title","validType":"","operation":"="},
)

"""
dnslist
"""
const.DNSLIST_COLUMNS=(
    Column('id','id',controltype='hidden',show=False),
    Column('dnsname','域名'),
    Column('type','类型', control="select",formatter = dnstypeformat,controltype='select',easyclass='easyui-combobox',source=dnstypelist),
    Column('describ','描述'),
)

const.DNSLIST_SEARCH = (
    {'name':'dnsname','title':'域名','validType':'','operation':'='},
)        

"""
EVILIP_LIST
"""
const.EVILIPLIST_COLUMNS=(
    Column('id','id',controltype='hidden',show=False),
    Column('startip','开始地址'),
    Column('endip','结束地址'),
    Column('describ','描述'),
)

const.EVILIPLIST_SEARCH = (
    {'name':'startip','title':'开始地址','validType':'','operation':'='},
)


"""
TRO_DNS
"""
const.TRODNS_COLUMNS=(
    Column('id','id',controltype='hidden',show=False),
    Column('dnsname','DNS'),
    Column('describ','描述'),
)

const.TRODNS_SEARCH = (
    {'name':'dnsname','title':'DNS','validType':'','operation':'='},
)

"""
TRO_IP
"""
const.TROIP_COLUMNS=(
    Column('id','id',controltype='hidden',show=False),
    Column('ip_addr','IP Addr'),
    Column('time','Time'),
    Column('describ','描述'),
)

const.TROIP_SEARCH = (
    {'name':'ip_addr','title':'IP Addr','validType':'','operation':'='},
)

"""
GLOBALPARA
"""
const.GLOBALPARA_COLUMNS=(
    Column('id','id',controltype='hidden',show=False),
    Column('beaterror','心跳偏差'),
    Column('beatcount','心跳次数',defaultvalue=5),
    Column('dnsttl','域名生存期',defaultvalue=60),
    Column('tcplasted','TCP长链接时间',defaultvalue=60),
    Column('tcpdivide','TCP链接内比值',defaultvalue=5),
    Column('tcpcount','TCP链接内次数',defaultvalue=5000),
    Column('httpsenddivide','HTTP发收比值',defaultvalue=5),
    Column('httppostdivide','HTTPPostGet比值',defaultvalue=5),
    Column('describ','描述'),
)

const.GLOBALPARA_SEARCH = (
   {'name':'beaterror','title':'beaterror','validType':'','operation':'='},
)

"""
ALARM
"""
const.ALARM_COLUMNS=(
    Column('id','id',controltype='hidden',show=False),
    Column('rid','rid',controltype='hidden',show=False,defaultvalue=0),
    Column('type','报警类别'),
    Column('class','报警级别'),
    Column('trojanid','木马号'),
    Column('dip','被控主机地址'),
    Column('dmac','被控主机MAC地址'),
    Column('sip','控制主机地址'),
    Column('scc','控制主机所在国家'),
    Column('time','报警时间'),
    Column('alarm_msg','报警描述'),
)

const.ALARM_SEARCH = (
   {'name':'type','title':'报警类别','validType':'','operation':'='},
)

"""
EVENT
"""
const.EVENT_COLUMNS=(
    Column('id','id',controltype='hidden',show=False),
    Column('pid','事件规则集号',controltype='hidden',show=False,defaultvalue=0),
    Column('psid','事件规则号',controltype='hidden',show=False,defaultvalue=0),
    Column('time','产生事件时间'),
    Column('risk','事件危险值'),
    Column('sip','外部主机地址'),
    Column('sport','外部主机端口'),
    Column('dip','内部主机地址'),
    Column('dmac','内部主机MAC地址'),
    Column('dport','内部主机端口'),
    Column('pro','协议'),
    Column('sflag','是否包含域名',controltype='hidden',show=False,defaultvalue=0),
    Column('extradata','事件描述'),
    Column('dns_name','事件相关的域名',controltype='hidden',show=False,defaultvalue=''),    
)

const.EVENT_SEARCH = (
   {'name':'type','title':'报警类别','validType':'','operation':'='},
)

const.entities = {
    "author":{"tablename":"authors","columns":const.AUTHOR_COLUMNS,"search":const.AUTHOR_SEARCH},
    "entry":{"tablename":"entries","columns":const.ENTRIES_COLUMNS,"search":const.ENTRIES_SEARCH},
    "dnslist":{"tablename":"DNS_LIST","columns":const.DNSLIST_COLUMNS,"search":const.DNSLIST_SEARCH},
    "evilip":{"tablename":"EVILIP_LIST","columns":const.EVILIPLIST_COLUMNS,"search":const.EVILIPLIST_SEARCH},
    "trodns":{"tablename":"TRO_DNS","columns":const.TRODNS_COLUMNS,"search":const.TRODNS_SEARCH},
    "troip": {"tablename":"TRO_IP","columns":const.TROIP_COLUMNS,"search":const.TROIP_SEARCH},
    "globalpara": {"tablename":"GLOBALPARA","columns":const.GLOBALPARA_COLUMNS,"search":const.GLOBALPARA_SEARCH},
    "alarm": {"tablename":"ALARM","columns":const.ALARM_COLUMNS,"search":const.ALARM_SEARCH},
    "event": {"tablename":"EVENT","columns":const.EVENT_COLUMNS,"search":const.EVENT_SEARCH}
}
