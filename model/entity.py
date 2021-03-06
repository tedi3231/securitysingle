#!/usr/bin/env python
#coding=utf8
'''
create and edit or remove entity from database
'''
import const,model
import tornado.database
from copy import copy
from datetime import datetime

db = None #tornado.database.Connection("127.0.0.1:3306","blog","root","password")

def _checkTable(entityName):
    result = {"result":"success", "message":""}
    if not entityName or entityName not in const.entities:
        result["result"] = "error"
        result["message"] = "no such tablename"
        return result
    return result

def _getColumnNamesAndTableName(entityName):
    return [item.field for item in const.entities[entityName]["columns"]], const.entities[entityName]["tablename"]

def _makeRemoveSql(entityName, entityId):
    tableName = const.entities[entityName]["tablename"]
    return str.format("DELETE FROM {0} WHERE id = {1}", tableName, entityId)

def _makeGetEntitySql(entityName, entityId):
    tableName = const.entities[entityName]["tablename"]
    return str.format("SELECT * FROM {0} WHERE id = {1}", tableName, entityId)

def _makeInsertSql(entityName, arguments):
    columnNames, tableName = _getColumnNamesAndTableName(entityName)  
    vals = {}
    for key in arguments:
        if key in columnNames:
            vals[key] = arguments[key][0]    
    sql = str.format("insert into {0}({1})values({2})", tableName, ",".join(vals.keys()), ",".join(["%s"] * len(vals.keys())))
    #print arguments
    #print sql
    return sql, vals     

def _makeUpdateSql(entityName, arguments):
    columnNames, tableName = _getColumnNamesAndTableName(entityName)          
    vals = {}
    for key in arguments:
        if key in columnNames:
            vals[key] = arguments[key][0]
    rowId = arguments["id"][0]
    sql = str.format("UPDATE {0} SET {1} WHERE id={2}", tableName, ",".join([str.format("{0}=%s", col) for col in vals.keys()]), rowId)    
    #print sql,vals
    return sql, vals     


def _makeWhereCondition(entityName, arguments):
    #print entityName
    #print const.entities[entityName]['search']
    columnNames = [item['name'].lower() for item in const.entities[entityName]["search"]]
    #print columnNames
    columns = const.entities[entityName]["search"]
    condition = []        
    #print entityName,columnNames,columns      
    #print columns
    #print "arguments %s" %arguments
    col = {}
    for arg in arguments:
        arg = arg.lower().strip()
        if arg in columnNames:
            val = arguments[arg][0]
            if not val.isspace():                    
                #print col
                col = [item for item in columns if item["name"] == arg][0]
                if col.has_key('formatter') and col['formatter']:
                    val = col['formatter'](val)
                if col["operation"] == "like":
                    condition.append(str.format("AND {0} like '%%{1}%%'", col['field'], val))
                elif col["operation"] == "=":
                    condition.append(str.format("AND {0} = '{1}'", col['field'], val))
                else:
                    print col['operation']
                    condition.append(str.format("AND {0} {1} {2}",col['field'],col['operation'],val))
    if len(condition) > 0 :
        condition.insert(0, "1=1 ")
    #print condition
    return " ".join(condition)


def createEntity(entityName, arguments):
    result = _checkTable(entityName)
    if result["result"] != "success":
        return result            
    sql, vals = _makeInsertSql(entityName, arguments)
    #print sql
    #print vals  
    if db.execute(sql, *vals.values()) < 0 :
        result["result"] = 'failed'
    return result

def editEntity(entityName, arguments):
    result = _checkTable(entityName)
    if result["result"] != "success":
        return result
    sql, vals = _makeUpdateSql(entityName, arguments)      
    if db.execute(sql, *(vals.values())) < 0 :
        result["result"] = 'failed'
    return result
        
def removeEntity(entityName, entityId):
    result = _checkTable(entityName)
    if result["result"] != "success":
        return result
    removeSql = _makeRemoveSql(entityName, entityId)
    if db.execute(removeSql) < 0:
        result["result"] = "error"        
    return result

def getEntity(entityName, entityId):
    result = _checkTable(entityName)
    #print result
    if result['result'] != 'success':
        return None
    getSql = _makeGetEntitySql(entityName, entityId)
    #print getSql
    return db.get(getSql)

def query(entityName, arguments):
    tablename = const.entities[entityName]["tablename"]   
    condition = _makeWhereCondition(entityName, arguments)
    page = int(arguments["page"][0]) - 1
    rows = int(arguments["rows"][0])
    totalQuery = ""
    rowsQuery = ""    
    if condition.strip() != '':
        totalQuery = str.format("select * from {0} where {1}", tablename, condition)
        rowsQuery = str.format("select * from {0} where {3} limit {1},{2}",
                                tablename, page * rows, rows, condition)
    else:
        totalQuery = str.format("select * from {0} ", tablename)
        rowsQuery = str.format("select * from {0} limit {1},{2}", tablename, page * rows, rows)   
    #print totalQuery
    #print rowsQuery
    total = db.execute_rowcount(totalQuery)
    datarows = db.query(rowsQuery)
    return total, datarows

def querySqlStr(sql):
    if not sql :
        return None
    return db.query(sql)

def queryall(entityName):
    """
    Query all data rows
    """
    tablename = const.entities[entityName]["tablename"]   
    rowsQuery = str.format("select * from {0} ", tablename)
    datarows = db.query(rowsQuery)
    return datarows

if __name__ == "__main__":
    #print removeEntity("author",1)
    #print _getInsertColumnNames("author")
    #print createEntity("author",{"name":["chyyy"],"email":["chy234@ks.com"]})
    #print _makeUpdateSql("author",{"name":["chyyy"],"email":["chy234@ks.com"],"id":[1]})
    #print editEntity("author",{"name":["addddd"],"email":["chy11111@ks.com"],"id":[2]})
    #print(_makeWhereCondition("author",{'name':['pancy']}))
    #print query("author",{"page":['1'],"rows":['10']})
    print getEntity("author", 1)
