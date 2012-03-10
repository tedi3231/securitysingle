#coding=utf8
"""
主要包含数据基本操作的Handler，如增删查改
"""
from basehandler import BaseHandler
from model import model
from datetime import datetime
import tornado.web

class TestReportHandler(BaseHandler):
    def get(self):
        self.render("reportbase.html")

    def post(self):
        pass


class AlarmBarReportHandler(BaseHandler):
    def get(self):
        self.render("report/alarmbar.html")


class AlarmBarReportDataHandler(BaseHandler):
    def post(self):
        pietype = self.get_argument("pietype","")
        condition = None

        sqlStr= """select h as category, count as categorycount from 
                  (
                        select count(a.trojanid) as count,{1} as h from ALARM as a WHERE {0} group by {1}
                  ) as test order by count desc {2};
                """

        byHour = "hour(from_unixtime(time))"
        byDay = "day(from_unixtime(time))"
        byMonth = "month(from_unixtime(time))"

        limitStr = " limit {0}"
        categories = {}
        groupStr = None
        if pietype == 'today':
            condition = str.format(" date(from_unixtime(time))='{0}'",datetime.now().strftime("%Y-%m-%d"))
            groupStr = byHour
            limitStr = str.format(limitStr,24)
            for item in range(24):
                categories[item]=0
        elif pietype=='currentmonth':
            condition = str.format(" EXTRACT(YEAR_MONTH FROM from_unixtime(time))='{0}'",datetime.now().strftime("%Y%m"))
            groupStr = byDay
            limitStr = str.format(limitStr,31)
            for item in range(1,31):
                categories[item]=0
        elif pietype == 'currentyear':
            condition = str.format(" year(from_unixtime(time))={0}",datetime.now().year)
            groupStr = byMonth
            limitStr = str.format(limitStr,12)
            for item in range(1,13):
                categories[item]=0
        
        sqlStr = str.format(sqlStr,condition,groupStr,limitStr)
        rows = self.db.query(sqlStr)
        data = {'category':categories,'data':[{'name':'警报次数','data':[]}]}
        #print tornado.web.escape.json_encode(data) 
        print categories
        if rows:
            d = {}
            for item in rows:
                d[item['category']]=item['categorycount']
            print d
            for item in categories:
                if item in d:
                    categories[item]=d[item]
            if pietype == 'today':
                data['category']=[(str(item)+"点") for item in categories.keys()]
            elif pietype=='currentmonth':
                data['category']=[(str(item)+"号") for item in categories.keys()]            
            elif pietype == 'currentyear':
                data['category']=[(str(item) + "月份") for item in categories.keys()]
            data['data'][0]['data']=categories.values()
        print tornado.web.escape.json_encode(data)
        self.write(tornado.web.escape.json_encode(data))
        #print rows
        #print categories.keys()
        #print categories.values()
        #print rows
        #print sqlStr
        #self.write("({'category':['0','1','2','3','4','5','6','7','8','9','10','11'],'data':[{name : '警报次数',data : [54,65,23,2,12,34,6,23,23,12,44,2]}]})")           


class AlarmPieReportHandler(BaseHandler):
    def get(self):
        self.render("report/alarmpie.html")

class PieReportDataBaseHandler(BaseHandler):
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

class AlarmReportDataHandler(PieReportDataBaseHandler):
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



