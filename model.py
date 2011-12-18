from griddata import Column
import const
'''
Authors table's columns
'''
const.AUTHOR_COLUMNS = [
            Column('name', 'First Name', "100", "left"),
            Column('email', 'Email', "100", "left"),
            Column('id', 'ID', "100", "left")
           ]

const.AUTHOR_SEARCH = (
    {"name":"name","title":"Name","validType":"","operation":"like"},
    {"name":"email","title":"Email","validType":"email","operation":"like"},    
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
           )

const.ENTRIES_SEARCH = (
    {"name":"slug","title":"slug","validType":"","operation":"like"},
    {"name":"title","title":"Title","validType":"","operation":"like"},
)
