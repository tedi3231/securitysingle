#coding=utf8
"""
主要包含数据基本操作的Module，查询、实体和列
"""
import tornado.web

class SearchModule(tornado.web.UIModule):
    def render(self, model):
        #print model
        return self.render_string("modules/search.html", model=model)

'''
for generate form
'''
class EntityModule(tornado.web.UIModule):
    def render(self, columns, entity=None):
        if entity:
            for col in columns:
                if entity.has_key(col.field):
                    col.defaultvalue = entity[col.field]
        return self.render_string("modules/entity.html", columns=columns, entity=entity)

class ColumnModule(tornado.web.UIModule):
    def render(self, column, value=None):
        return self.render_string("modules/column.html", column=column, value=value)