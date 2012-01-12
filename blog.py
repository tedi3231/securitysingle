#!/usr/bin/env python
#coding=utf8
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import markdown
import os.path
import re
import tornado.auth
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
from tornado.options import define, options
from datetime import datetime
from schema import Column, GridData
import model
import const
import entity

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="security", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="password", help="blog database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/author/list", AllAuthorsHandler),
            (r"/entry/list", EntriesHandler),
            (r"/data/create", CreateFormHandler),
            (r"/data/remove", RemoveHandler),
            (r"/data/edit", EditHandler),
            (r"/dns/list", DNSListHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
        ]
        settings = dict(
            denug=True,
            blog_title=u"无锡安全信息专家委員会",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Entry": EntryModule, "Search":SearchModule, "Entity":EntityModule, "Column":ColumnModule},
            xsrf_cookies=True,
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)
        entity.db = self.db

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))

    def griddata(self, entityName):
        total, datarows = entity.query(entityName, self.request.arguments)
        gd = GridData()
        gd['total'] = total
        gd['rows'] = datarows
        print total
        print datarows
        return tornado.escape.json_encode(gd)

class RemoveHandler(BaseHandler):
    def post(self):
        entityname = self.get_argument("entityname", "")       
        entityId = self.get_argument("id", "0")
        print entityname, entityId
        result = entity.removeEntity(entityname, entityId)
        self.write(tornado.escape.json_encode(result))

class EditHandler(BaseHandler):
    def get(self):
        entityname = self.get_argument("entityname", "")       
        entityid = self.get_argument("id", "")
        row = entity.getEntity(entityname, entityid)
        print row
        columns = const.entities[entityname]['columns']        
        return self.render("edit.html", entityname=entityname, columns=columns, entity=row)

    def post(self):
        entityname = self.get_argument("entityname", "")
        result = entity.editEntity(entityname, self.request.arguments)
        self.write(tornado.escape.json_encode(result))

class CreateFormHandler(BaseHandler):
    def getEntityNameAndColumns(self):
        entityname = self.get_argument("entityname", "")       
        columns = const.entities[entityname]["columns"]     
        return (entityname, columns)

    def get(self):
        entityname, columns = self.getEntityNameAndColumns()
        self.render("create.html", columns=columns, entityname=entityname)

    def post(self):
        entityname = self.get_argument("entityname", "")
        result = entity.createEntity(entityname, self.request.arguments)
        self.write(tornado.escape.json_encode(result))

class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html")

class AllAuthorsHandler(BaseHandler):
    def get(self):                
        self.render("griddata.html", entityname="author", url="/author/list",
                    title="All Authors", rownumbers="true", pagination="true",
                    columns=const.AUTHOR_COLUMNS, search_columns=const.AUTHOR_SEARCH)        
        
    def post(self):
        self.write(self.griddata("author"))


class EntriesHandler(BaseHandler):
    def get(self):
        self.render("griddata.html", entityname="entry",
        url="/entry/list", title="All Entries",
        rownumbers="true", pagination="true",
        columns=const.ENTRIES_COLUMNS, search_columns=const.ENTRIES_SEARCH)        
        
    def post(self):        
        self.write(self.griddata("entry"))

class DNSListHandler(BaseHandler):
    def get(self):
        entityname = 'dnslist'
        self.render("griddata.html", entityname=entityname,
        url="/dns/list", title="All dns",
        rownumbers="true", pagination="true",
        columns=const.entities[entityname]['columns'], search_columns=const.entities[entityname]['search'])        
        
    def post(self):        
        self.write(self.griddata("dnslist"))

class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()
    
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        author = self.db.get("SELECT * FROM authors WHERE email = %s",
                             user["email"])
        if not author:
            # Auto-create first author
            any_author = self.db.get("SELECT * FROM authors LIMIT 1")
            if not any_author:
                author_id = self.db.execute(
                    "INSERT INTO authors (email,name) VALUES (%s,%s)",
                    user["email"], user["name"])
            else:
                self.redirect("/")
                return
        else:
            author_id = author["id"]
        self.set_secure_cookie("user", str(author_id))
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)

'''
for generate search form
'''
class SearchModule(tornado.web.UIModule):
    def render(self, model):
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

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
