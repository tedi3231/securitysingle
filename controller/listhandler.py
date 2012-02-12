#coding=utf8
from basehandler import BaseHandler
from model import entity
import tornado.web

class DNSListHandler(BaseHandler):    
    def get(self):        
        self.rendergriddata('dnslist', '域名配置', '/dns/list')
        
    def post(self):        
        self.write(self.griddata("dnslist"))

class EVILIPListHandler(BaseHandler):
    def get(self):        
        self.rendergriddata('evilip', '恶意地址', '/evilip/list')
        
    def post(self):        
        self.write(self.griddata("evilip"))

class TRODNSHandler(BaseHandler):
    def get(self):
        self.rendergriddata('trodns', 'DNS木马触发器', '/trodns/list')
        
    def post(self):        
        self.write(self.griddata("trodns"))

class TROIPHandler(BaseHandler):
    def get(self):      
        self.rendergriddata('troip', '木马触发器', '/troip/list')
                
    def post(self):        
        self.write(self.griddata("troip"))

class GLOBALPARAHandler(BaseHandler):
    def get(self):
        self.rendergriddata('globalpara', '检测参数', '/globalpara/list',canAdd=False, canEdit=True, canRemove=False)
        
    def post(self):        
        self.write(self.griddata("globalpara"))

class ALARMHandler(BaseHandler):
    def get(self):        
        self.rendergriddata('alarm', '报警信息', '/alarm/list', canAdd=False, canRemove=False, canEdit=False,showsearch=False)
        
    def post(self):        
        self.write(self.griddata("alarm"))

class EVENTHandler(BaseHandler):
    def get(self):        
        self.rendergriddata('event', '事件子因', '/event/list', canAdd=False, canRemove=False, canEdit=False,showsearch=False)
        
    def post(self):        
        self.write(self.griddata("event"))

class ALARMAnalyseHandler(BaseHandler):
    def get(self):        
        self.rendergriddata('alarm_1', '报警信息', '/alarm/analyse', canAdd=False, canRemove=False, canEdit=False,showsearch=True)
        
    def post(self):        
        self.write(self.griddata("alarm_1"))

class EVENTAnalyseHandler(BaseHandler):
    def get(self):        
        self.rendergriddata('event_1', '事件子因', '/event/analyse', canAdd=False, canRemove=False, canEdit=False,showsearch=True)
        
    def post(self):        
        self.write(self.griddata("event_1"))

        
class USER_TROJAN_RULEHandler(BaseHandler):
    def get(self):        
        self.rendergriddata('usertrojanrule', '事件子因', '/usertrojanrule/list', canAdd=True, canRemove=False, canEdit=True)
        
    def post(self):        
        self.write(self.griddata("usertrojanrule")) 

class USERSHandler(BaseHandler):
    def get(self):        
        self.rendergriddata('users', '用户信息', '/users/list', canAdd=True, canRemove=False, canEdit=True)
        
    def post(self):        
        self.write(self.griddata("users")) 

class RESOURCESHandler(BaseHandler):
    def get(self):        
        self.rendergriddata('resources', '资源信息', '/resources/list', canAdd=True, canRemove=True, canEdit=True)
        
    def post(self):        
        self.write(self.griddata("resources"))

class PERMISIONHandler(BaseHandler):
    def get(self):        
        self.rendergriddata('permision', '资源信息', '/permision/list', canAdd=True, canRemove=True, canEdit=True,
                            addAction="/permision/create",editAction="/permision/create")
        
    def post(self):        
        self.write(self.griddata("permision"))

class PERMISIONEditHandler(BaseHandler):
    def get(self):
        entityId = self.get_argument("id", "0")
        entityItem = None
        print entityId
        if entityId <> "0":
            entityItem = entity.getEntity("permision",entityId)  
        else:
            entityItem = {"id":"","userid":"","resourceid":""}      
        users = entity.queryall("users")
        resources = entity.queryall("resources")
        self.render("permisionedit.html",pitem=entityItem,users=users,controllers=resources)

    def post(self):
        entityname = "users_resources"
        arguments = self.beforesaveformat(entityname, self.request.arguments)
        result = {}
        if arguments.has_key("id") and arguments['id'][0] and int(arguments['id'][0])>0:
            result = entity.editEntity(entityname, arguments)            
        else:
            result = entity.createEntity(entityname, arguments)
        if result['result']=='success':
            self.afterSave(entityname,arguments)
            self.writeLog("create",entityname,str(arguments))      
        self.write(tornado.escape.json_encode(result))        

class LOGINFOHandler(BaseHandler):
    def get(self):        
        self.rendergriddata('loginfo', '日志信息', '/loginfo/list', canAdd=False, canRemove=False, canEdit=False)
        
    def post(self):        
        self.write(self.griddata("loginfo"))
