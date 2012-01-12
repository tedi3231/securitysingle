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

const.ENTRIES_SEARCH = (
    {"name":"slug","title":"slug","validType":"","operation":"="},
    {"name":"title","title":"Title","validType":"","operation":"="},
)

const.entities = {
    "author":{"tablename":"authors","columns":const.AUTHOR_COLUMNS,"search":const.AUTHOR_SEARCH},
    "entry":{"tablename":"entries","columns":const.ENTRIES_COLUMNS,"search":const.ENTRIES_SEARCH},
    "dnslist":{"tablename":"DNS_LIST","columns":const.DNSLIST_COLUMNS,"search":const.DNSLIST_SEARCH}
}
