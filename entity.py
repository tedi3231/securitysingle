#!/usr/bin/env python
#coding=utf8
'''
create and edit or remove entity from database
'''
import const
import model
import tornado.database
from copy import copy

db = tornado.database.Connection("127.0.0.1:3306","blog","root","password")

def _checkTable(entityName):
    result = {"result":"success","message":""}
    if not entityName or entityName not in const.entities:
        result["result"] = "error"
        result["message"] = "no such tablename"
        return result
    return result

def _getColumnNamesAndTableName(entityName):
    return [item['field'] for item in const.entities[entityName]["columns"] if item["noscaler"]==False],const.entities[entityName]["tablename"]

def _makeRemoveSql(entityName,entityId):
    tableName = const.entities[entityName]["tablename"]
    return str.format("DELETE FROM {0} WHERE id = {1}",tableName,entityId)

def _makeInsertSql(entityName,arguments):
    columnNames,tableName = _getColumnNamesAndTableName(entityName)   
    vals = {}
    for key in arguments:
        if key in columnNames:
            vals[key] = arguments[key][0]    
    sql = str.format("insert into {0}({1})values({2})",tableName,",".join(vals.keys()),",".join(["%s"]*len(vals.keys())))
    return sql,vals     

def _makeUpdateSql(entityName,arguments):
    columnNames,tableName =  _getColumnNamesAndTableName(entityName)
    columnNames.append("id")        
    vals = {}
    for key in arguments:
        if key in columnNames:
            vals[key] = arguments[key][0]
    columnNames.remove("id")   
    sql = str.format("UPDATE {0} SET {1} WHERE id={2}",tableName,",".join([str.format("{0}=%s",col) for col in columnNames]),vals["id"])    
    return sql,vals     


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
    del vals["id"]
    print sql,vals
    if db.execute(sql,*vals.values()) <0 :
        result["result"]='failed'
    return result
        
def removeEntity(entityName,entityId):
    result = _checkTable(entityName)
    if result["result"] != "success":
        return result
    removeSql = _makeRemoveSql("author",entityId)
    if db.execute(removeSql)<0:
        result["result"] = "error"        
    return result

if __name__ == "__main__":
    #print removeEntity("author",1)
    #print _getInsertColumnNames("author")
    #print createEntity("author",{"name":["chyyy"],"email":["chy234@ks.com"]})
    #print _makeUpdateSql("author",{"name":["chyyy"],"email":["chy234@ks.com"],"id":[1]})
    print editEntity("author",{"name":["dddddd"],"email":["chy00000@ks.com"],"id":[2]})
