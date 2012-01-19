#!/usr/bin/env python
#coding=utf8
import model
import const
import entity
import unittest
from copy import copy

succResult = {"result":"success","message":""}
failedResult = {"result":"error","message":""}

class TestRemoveEntityFunction(unittest.TestCase):    

    def testSimple(self):
        result = entity.removeEntity("authors",1)
        self.assertEqual(succResult,result,str.format("expected {0} ,fatual {1}",succResult,result))


class TestCheckTable(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def testSimple(self):
        result = entity.checkTable("authors")
        self.assertEqual(succResult,result,str.format("expected {0} ,fatual {1}",succResult,result))

class TestmakeRemoveSql(unittest.TestCase):
    def testSimple(self):
        result = entity.makeRemoveSql("authors",1)
        self.assertEqual("DELETE FROM authors WHERE id = 1",result)

if __name__ == "__main__":
    unittest.main()
