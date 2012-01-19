#coding=utf8
"""
主要包含数据基本操作的Handler，如增删查改
"""
from basehandler import BaseHandler
from lib import hardwareinfo

class SystemHandler(BaseHandler):    
    def get(self):        
        self.render("systeminfo.html",meminfo=hardwareinfo.getMemoryInfo(),diskinfo=hardwareinfo.get_df_data("/var"),time_info=hardwareinfo.get_time_info(),networkinfo=hardwareinfo.getNetworkInfo() )
    