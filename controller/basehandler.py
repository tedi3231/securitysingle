#coding=utf8
"""
主要包含数据基本操作的Handler，如增删查改
"""
from datetime import datetime
import tornado.web
import tornado.auth
from model import const,entity
from model.schema import Column, GridData

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        #return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))
        return 'tedi3231'   
    
    def beforesaveformat(self,entityname,arguments):
        colformats = {}
        for col in  const.entities[entityname]['columns']:
            if col.saveformatter is not None:
                colformats[col.field] = col.saveformatter                                
        for k in arguments:           
            if k in colformats:                               
                arguments[k][0] = colformats[k](arguments[k][0])                
        return arguments

    def afterSave(self,entityname,arguments):
        """
        when add or edit method excutes success,call it
        """
        if const.entities[entityname].has_key("aftersave") and const.entities[entityname]['aftersave']:
            const.entities[entityname]['aftersave']()    

    def beforeshowentityformat(self,entityname,item):
        colformats = {}
        for col in  const.entities[entityname]['columns']:
            if col.formatter is not None:
                colformats[col.field] = col.formatter                                
        for k in item:           
            if k in colformats:                               
                item[k] = colformats[k](item[k])                
        return item        
    
    def beforeshowgridformat(self,entityname,rows):
        columns = const.entities[entityname]["columns"]
        formatColumns = [{item.field:item.formatter} for item in columns if item.formatter]
        #print total,datarows
        for item in rows:
            for k in item:
                if type(item[k]) is datetime:
                    item[k] = item[k].strftime("%Y-%m-%d")
                #call formatter method
                for fitem in formatColumns:
                    if k in fitem:
                        item[k] = fitem[k](item[k])
        #print total,datarows
        return rows

    def writeLog(self,action,entityname,msg):
        content = str.format("{0} at {1} {4} {2},values is {3}",self.get_current_user(),datetime.now().isoformat(),
                             const.entities[entityname]['tablename'],msg,action)
        print content
        arguments = {"content":[content],"createtime":[datetime.now()]}
        result = entity.createEntity("loginfo", arguments)
        print result
    
    def griddata(self, entityName):
        total, datarows = entity.query(entityName, self.request.arguments)
        datarows = self.beforeshowgridformat(entityName,datarows)
        gd = GridData()
        gd['total'] = total
        gd['rows'] = datarows        
        return tornado.escape.json_encode(gd)
    
    def rendergriddata(self, entityname, title, url, canAdd=True, canEdit=True, canRemove=True,showsearch=True):
        columns = const.entities[entityname]['columns']
        search_columns = const.entities[entityname]['search']
        if showsearch <> True:
            search_columns = []
        self.render("griddata.html", entityname=entityname, url=url, title=title,
                    rownumbers="true", pagination="true", columns=columns,
                    search_columns=search_columns, canAdd=canAdd, canEdit=canEdit, canRemove=canRemove
                   )

class RemoveHandler(BaseHandler):
    def post(self):
        entityname = self.get_argument("entityname", "")       
        entityId = self.get_argument("id", "0")
        print entityname, entityId
        result = entity.removeEntity(entityname, entityId)
        if result['result']=='success':
            self.writeLog( "remove",entityname,str(arguments))
        self.write(tornado.escape.json_encode(result))

class EditHandler(BaseHandler):
    def get(self):
        entityname = self.get_argument("entityname", "")       
        entityid = self.get_argument("id", "")
        row = entity.getEntity(entityname, entityid)
        row = self.beforeshowentityformat(entityname, row)
        print row
        columns = const.entities[entityname]['columns']        
        return self.render("edit.html", entityname=entityname, columns=columns, entity=row)

    def post(self):
        entityname = self.get_argument("entityname", "")
        arguments = self.beforesaveformat(entityname, self.request.arguments)
        result = entity.editEntity(entityname, arguments)
        if result['result']=='success':
            self.afterSave(entityname,arguments)
            self.writeLog("update", entityname,str(arguments))
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
        arguments = self.beforesaveformat(entityname, self.request.arguments)
        result = entity.createEntity(entityname, arguments)
        if result['result']=='success':
            self.afterSave(entityname,arguments)
            self.writeLog("create",entityname,str(arguments))      
        self.write(tornado.escape.json_encode(result))
        

class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))        


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

