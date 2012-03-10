#coding=utf8
"""
主要包含数据基本操作的Handler，如增删查改
"""
from basehandler import BaseHandler
from lib import hardwareinfo

class SystemHandler(BaseHandler):    
    def get(self):        
        self.render("systeminfo.html",meminfo=hardwareinfo.getMemoryInfo(),diskinfo=hardwareinfo.get_df_data("/var"),time_info=hardwareinfo.get_time_info(),networkinfo=hardwareinfo.getNetworkInfo() )
    
class TestAjaxHandler(BaseHandler):
    def get(self):
        self.write("[{name : 'PanChunYan',data : [12, 12, 12]},{name : 'Zhangw',data : [2, 3, 5]}]")
        
class ChartTestHandler(BaseHandler):
    def get(self):
        self.render("report/chartbar.html")

class PieChartTestHandler(BaseHandler):
    def get(self):
        self.render("report/piechart.html")
