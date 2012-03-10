#coding=utf8
"""
主要包含数据基本操作的Handler，如增删查改
"""
from basehandler import BaseHandler
from model import model
from datetime import datetime

class TestReportHandler(BaseHandler):
    def get(self):
        self.render("reportbase.html")

    def post(self):
        pass

class AlarmPieReportHandler(BaseHandler):
    def get(self):
        self.render("report/alarmpie.html")

class ReportDataBaseHandler(BaseHandler):
    def formatDataToJson(self,rows,catogery,catogeryFormat,valuename):
        if not rows or len(rows)<=0:
            return ""
        data = [{item[catogery]:item[valuename] for item in rows}]
        if catogeryFormat:
            strList = ['["'+ (isinstance(catogeryFormat(key),unicode) and catogeryFormat(key) or str(catogeryFormat(key)))  +'",' + str(data[0][key])+']'  for key in data[0]]
        else:
            strList = ['["'+ (isinstance(key,unicode) and key or str(key))+'",' + str(data[0][key]) +']' for key in data[0]]
        print strList
        return "[" + ",".join(strList) + "]"

class AlarmReportDataHandler(ReportDataBaseHandler):
    def post(self):
        pietype = self.get_argument("pietype","")
        startTime = self.get_argument("starttime","")
        endTime = self.get_argument("endtime","")

        if startTime:
            startTime = model.convertDateStrToInt(startTime)
        else:
            startTime = model.convertDateStrToInt(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if endTime:
            endTime = model.convertDateStrToInt(endTime)
        else:
            endTime = model.convertDateStrToInt(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        condition = str.format( " time between {0} and {1} ",startTime,endTime )
        catogeryFormat = None
        if pietype=='level':
            sqlStr = "SELECT class as category,count(class) as categorycount FROM ALARM WHERE"+condition+" GROUP BY class"
            catogeryFormat = model.alarmlevelformat
        elif pietype=='type':
            sqlStr = "SELECT type as category,count(type) as categorycount FROM ALARM WHERE"+condition+" GROUP BY type"
            catogeryFormat = model.alarmtypeformat
        elif pietype=='trojan':
            sqlStr=str.format("""SELECT * FROM (SELECT u.troname as category,count(a.trojanid) as categorycount 
                             FROM ALARM as a ,USER_TROJAN_RULE as u where a.trojanid=u.id and {0} GROUP BY a.trojanid) as Test 
                             Order by categorycount desc limit 10""",condition)
        rows = self.db.query(sqlStr)    
        self.write( self.formatDataToJson(rows, "category",catogeryFormat,"categorycount"))



