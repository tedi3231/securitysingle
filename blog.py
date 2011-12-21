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
from griddata import Column, toGridViewHtml, GridData

from tornado.options import define, options
from datetime import datetime
import model
import const

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="password", help="blog database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/archive", ArchiveHandler),
            (r"/feed", FeedHandler),
            (r"/all", AllHandler),
            (r"/authors", AllAuthorsHandler),
            (r"/entries", EntriesHandler),
            (r"/entry/([^/]+)", EntryHandler),
            (r"/compose", ComposeHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
        ]
        settings = dict(
            denug = True,
            blog_title=u"无锡安全信息专家委員会",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Entry": EntryModule,"Search":SearchModule},
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


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))

    def makeWhereCondition(self,tableName):
        arguments = self.request.arguments
        columnNames = []
        columns = []
        condition = []        
        if tableName.lower() == "authors":
            columnNames = [item['name'] for item in const.AUTHOR_SEARCH]
            columns = const.AUTHOR_SEARCH
        elif tableName.lower() == "entries":          
            columnNames = [item['name'] for item in const.ENTRIES_SEARCH]
            columns = const.ENTRIES_SEARCH       
        col = {}
        for arg in arguments:
            arg = arg.lower().strip()
            if arg in columnNames:
                val = arguments[arg][0]
                if not val.isspace():                    
                    col = [item for item in columns if item["name"] == arg][0]
                    if col["operation"] == "like":
                        condition.append(str.format("AND {0} like '%{1}%'",arg,val))
                    elif col["operation"] == "=":
                        condition.append(str.format("AND {0} = '{1}'",arg,val))
        if len(condition) > 0 :
            condition.insert(0,"1=1 ")
        return " ".join(condition)


    def griddata(self,tablename):
        #print type(self.request.arguments)
        #print "condition---"
        condition = self.makeWhereCondition("authors")
        #print condition
        page = int(self.get_argument("page", 1))-1
        rows = int(self.get_argument("rows",10))
        totalQuery = ""
        rowsQuery = ""
        #print str.format("|{0}|",condition)
        if condition.strip()!='':
            totalQuery = str.format("select * from {0} where {1}",tablename,condition)
            rowsQuery =  str.format("select * from {0} where {3} limit {1},{2}",tablename,page*rows,rows,condition)
        else:
            totalQuery = str.format("select * from {0} ",tablename)
            rowsQuery =  str.format("select * from {0} limit {1},{2}",tablename,page*rows,rows)
        print totalQuery, rowsQuery 
        total = self.db.execute_rowcount(totalQuery)
        datarows = self.db.query(rowsQuery)
        print total,datarows
        for item in datarows:
            for k in item:
                if type(item[k]) is datetime:
                    item[k] = item[k].strftime("%Y-%m-%d")
        gd = GridData()
        gd['total'] = total
        gd['rows'] = datarows
        return tornado.escape.json_encode(gd)

class HomeHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC LIMIT 5")
        if not entries:
            self.redirect("/compose")
            return
        self.render("home.html", entries=entries)

class AllHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published ")       
        self.render("home.html", entries=entries)   

class AllAuthorsHandler(BaseHandler):
    def get(self):                
        self.render("griddata.html", tableid="authors", url="/authors", 
                    title="All Authors", rownumbers="true", pagination="true",
                    columns=const.AUTHOR_COLUMNS,search_columns=const.AUTHOR_SEARCH)        
        
    def post(self):
	print(self.request.arguments)
        self.write(self.griddata("authors"))

class EntriesHandler(BaseHandler):
    def get(self):
        self.render("griddata.html", tableid="entries", 
        url="/entries", title="All Entries",
        rownumbers="true", pagination="true", 
        columns=const.ENTRIES_COLUMNS,search_columns=const.ENTRIES_SEARCH)        
        
    def post(self):
        self.write(self.griddata("entries"))
        
        
class EntryHandler(BaseHandler):
    def get(self, slug):
        entry = self.db.get("SELECT * FROM entries WHERE slug = %s", slug)
        if not entry: raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=entry)


class ArchiveHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC")
        self.render("archive.html", entries=entries)


class FeedHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC LIMIT 10")
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)


class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        entry = None
        if id:
            entry = self.db.get("SELECT * FROM entries WHERE id = %s", int(id))
        self.render("compose.html", entry=entry)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        html = markdown.markdown(text)
        if id:
            entry = self.db.get("SELECT * FROM entries WHERE id = %s", int(id))
            if not entry: raise tornado.web.HTTPError(404)
            slug = entry.slug
            self.db.execute(
                "UPDATE entries SET title = %s, markdown = %s, html = %s "
                "WHERE id = %s", title, text, html, int(id))
        else:
            slug = unicodedata.normalize("NFKD", title).encode(
                "ascii", "ignore")
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())
            if not slug: slug = "entry"
            while True:
                e = self.db.get("SELECT * FROM entries WHERE slug = %s", slug)
                if not e: break
                slug += "-2"
            self.db.execute(
                "INSERT INTO entries (author_id,title,slug,markdown,html,"
                "published) VALUES (%s,%s,%s,%s,%s,UTC_TIMESTAMP())",
                self.current_user.id, title, slug, text, html)
        self.redirect("/entry/" + slug)


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

class SearchModule(tornado.web.UIModule):
   def render(self,model):
	return self.render_string("modules/search.html",model=model)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
