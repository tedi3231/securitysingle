#!/usr/bin/env python
#coding=utf8
'''
create and edit or remove entity from database
'''
import const
import model
import tornado.database
from copy import copy
from datetime import datetime

db = tornado.database.Connection("127.0.0.1:3306","blog","root","password")

def _checkTable(entityName):
    result = {"result":"success","message":""}
    if not entityName or entityName not in const.entities:
        result["result"] = "error"
        result["message"] = "no such tablename"
        return result
    return result

def _getColumnNamesAndTableName(entityName):
    return [item.field for item in const.entities[entityName]["columns"]],const.entities[entityName]["tablename"]

def _makeRemoveSql(entityName,entityId):
    tableName = const.entities[entityName]["tablename"]
    return str.format("DELETE FROM {0} WHERE id = {1}",tableName,entityId)

def _makeGetEntitySql(entityName,entityId):
    tableName = const.entities[entityName]["tablename"]
    return str.format("SELECT * FROM {0} WHERE id = {1}",tableName,entityId)

def _makeInsertSql(entityName,arguments):
    columnNames,tableName = _getColumnNamesAndTableName(entityName)  
    vals = {}
    for key in arguments:
        if key in columnNames:
            vals[key] = arguments[key][0]    
    sql = str.format("insert into {0}({1})values({2})",tableName,",".join(vals.keys()),",".join(["%s"]*len(vals.keys())))
    #print arguments
    #print sql
    return sql,vals     

def _makeUpdateSql(entityName,arguments):
    columnNames,tableName = _getColumnNamesAndTableName(entityName)          
    vals = {}
    for key in arguments:
        if key in columnNames:
            vals[key] = arguments[key][0]
    rowId = arguments["id"][0]
    sql = str.format("UPDATE {0} SET {1} WHERE id={2}",tableName,",".join([str.format("{0}=%s",col) for col in vals.keys()]),rowId)    
    #print sql,vals
    return sql,vals     


def _makeWhereCondition(entityName,arguments):
    columnNames = [item['name'].lower() for item in const.entities[entityName]["search"]]
    columns = const.entities[entityName]["search"]
    condition = []        
    #print entityName,columnNames,columns       
    col = {}
    for arg in arguments:
        arg = arg.lower().strip()
        if arg in columnNames:
            val = arguments[arg][0]
            if not val.isspace():                    
                col = [item for item in columns if item["name"] == arg][0]
                if col["operation"] == "like":
                    condition.append(str.format("AND {0} like '%%{1}%%'",arg,val))
                elif col["operation"] == "=":
                    condition.append(str.format("AND {0} = '{1}'",arg,val))
    if len(condition) > 0 :
        condition.insert(0,"1=1 ")
    #print condition
    return " ".join(condition)


def createEntity(entityName,arguments):
    result = _checkTable(entityName)
    if result["result"] != "success":
        return result
    sql,vals = _makeInsertSql(entityName,arguments)  
    if db.execute(sql,*vals.values()) <0 :
        result["result"]='failed'
    return result

def editEntity(entityName,arguments):
    result = _checkTable(entityName)
    if result["result"] != "success":
        return result
    sql,vals = _makeUpdateSql(entityName,arguments)      
    if db.execute(sql,*(vals.values())) <0 :
        result["result"]='failed'
    return result
        
def removeEntity(entityName,entityId):
    result = _checkTable(entityName)
    if result["result"] != "success":
        return result
    removeSql = _makeRemoveSql(entityName,entityId)
    if db.execute(removeSql)<0:
        result["result"] = "error"        
    return result

def getEntity(entityName,entityId):
    result = _checkTable(entityName)
    #print result
    if result['result'] !='success':
        return None
    getSql = _makeGetEntitySql(entityName,entityId)
    #print getSql
    return db.get(getSql)

def query(entityName,arguments):
    tablename = const.entities[entityName]["tablename"]
    
    columns = const.entities[entityName]["columns"]
    formatColumns= [{item.field:item.formatter} for item in columns if item.formatter]
    print formatColumns
     
    condition = _makeWhereCondition(entityName,arguments)
    page = int(arguments["page"][0])-1
    rows = int(arguments["rows"][0])
    totalQuery = ""
    rowsQuery = ""
    #print str.format("|{0}|",condition)
    if condition.strip()!='':
        totalQuery = str.format("select * from {0} where {1}",tablename,condition)
        rowsQuery =  str.format("select * from {0} where {3} limit {1},{2}",
                                tablename,page*rows,rows,condition)
    else:
        totalQuery = str.format("select * from {0} ",tablename)
        rowsQuery =  str.format("select * from {0} limit {1},{2}",tablename,page*rows,rows)
    #print totalQuery, rowsQuery 
    total = db.execute_rowcount(totalQuery)
    datarows = db.query(rowsQuery)
    #print total,datarows
    for item in datarows:
        for k in item:
            if type(item[k]) is datetime:
                item[k] = item[k].strftime("%Y-%m-%d")
            #call formatter method
            for fitem in formatColumns:
                if k in fitem:
                    item[k] = fitem[k](item[k])
    #print total,datarows
    return total,datarows

if __name__ == "__main__":
    #print removeEntity("author",1)
    #print _getInsertColumnNames("author")
    #print createEntity("author",{"name":["chyyy"],"email":["chy234@ks.com"]})
    #print _makeUpdateSql("author",{"name":["chyyy"],"email":["chy234@ks.com"],"id":[1]})
    #print editEntity("author",{"name":["addddd"],"email":["chy11111@ks.com"],"id":[2]})
    #print(_makeWhereCondition("author",{'name':['pancy']}))
    #print query("author",{"page":['1'],"rows":['10']})
    print getEntity("author",1)
