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

'''
Entries table's columns 
'''
const.ENTRIES_COLUMNS = [
            Column('slug', 'Slug', "100", "left"),
            Column('title', 'title', "100", "left"),
            Column('markdown', 'markdown', "100", "left"),
            Column('html', 'html', "100", "left"),
            Column('published', 'published', "100", "left"),
            Column('updated', 'updated', "100", "left")
           ]
