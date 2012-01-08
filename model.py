#from griddata import Column
from schema import Column
import const

author_list = {'rows':[{'name':'  ','id':' '},{'name':'tedi3231','id':'2'}],'valuetext':'name','valuename':'id'}
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
            Column('author_id', 'author_id',control="select",source=author_list,easyclass="easyui-combobox"),
            Column('id', 'ID', controltype='hidden',show=False),
           )

const.ENTRIES_SEARCH = (
    {"name":"slug","title":"slug","validType":"","operation":"="},
    {"name":"title","title":"Title","validType":"","operation":"="},
)

const.entities = {
    "author":{"tablename":"authors","columns":const.AUTHOR_COLUMNS,"search":const.AUTHOR_SEARCH},
    "entry":{"tablename":"entries","columns":const.ENTRIES_COLUMNS,"search":const.ENTRIES_SEARCH}
}
