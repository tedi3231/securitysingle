#from griddata import Column
from schema import Column
import const
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
            Column('slug', 'Slug', "100", "left"),
            Column('title', 'title', "100", "left"),
            Column('markdown', 'markdown', "100", "left"),
            Column('html', 'html', "100", "left"),
            Column('published', 'published', "100", "left"),
            Column('updated', 'updated', "100", "left"),
            Column('author_id', 'author_id', "100", "left"),
            Column('id', 'ID', "100", "left",True),
           )

const.ENTRIES_SEARCH = (
    {"name":"slug","title":"slug","validType":"","operation":"="},
    {"name":"title","title":"Title","validType":"","operation":"="},
)

const.entities = {
    "author":{"tablename":"authors","columns":const.AUTHOR_COLUMNS,"search":const.AUTHOR_SEARCH},
    "entry":{"tablename":"entries","columns":const.ENTRIES_COLUMNS,"search":const.ENTRIES_SEARCH}
}
