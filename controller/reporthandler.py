#coding=utf8
"""
主要包含数据基本操作的Handler，如增删查改
"""
from basehandler import BaseHandler

class TestReportHandler(BaseHandler):
    def get(self):
        self.render("reportbase.html")

    def post(self):
        pass
