#coding=utf8
import os
import re
import tornado.options
from tornado.options import define, options
from controller import basehandler,listhandler,otherhandler
from module.webmodule import SearchModule,EntityModule,ColumnModule

define("port", default=9999, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="security", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="password", help="blog database password")

handlers = [
            (r"/", basehandler.HomeHandler),
            (r"/data/create", basehandler.CreateFormHandler),
            (r"/data/remove", basehandler.RemoveHandler),
            (r"/data/edit", basehandler.EditHandler),
            (r"/dns/list", listhandler.DNSListHandler),
            (r"/evilip/list", listhandler.EVILIPListHandler),
            (r"/trodns/list", listhandler.TRODNSHandler),
            (r"/troip/list", listhandler.TROIPHandler),
            (r"/globalpara/list", listhandler.GLOBALPARAHandler),
            (r"/alarm/list", listhandler.ALARMHandler),
            (r"/event/list",listhandler.EVENTHandler),
            (r"/alarm/analyse", listhandler.ALARMAnalyseHandler),
            (r"/event/analyse",listhandler.EVENTAnalyseHandler),
            (r"/usertrojanrule/list",listhandler.USER_TROJAN_RULEHandler),
            (r"/users/list",listhandler.USERSHandler),
            (r"/resources/list",listhandler.RESOURCESHandler),
            (r"/loginfo/list",listhandler.LOGINFOHandler),
            (r"/system/info",otherhandler.SystemHandler),
            (r"/auth/login", basehandler.AuthLoginHandler),
            (r"/auth/logout", basehandler.AuthLogoutHandler),
        ]

settings = dict(
    denug=True,
    blog_title=u"This is an demo app",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    ui_modules={"Search":SearchModule, "Entity":EntityModule, "Column":ColumnModule},
    xsrf_cookies=True,
    cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    #login_url="/auth/login",
    autoescape=None,
)
