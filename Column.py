#coding=utf8

class Column(object):
    def __init__(self,field,title,width=100,align="left",control="text",easyclass="",source=None,formatter=None):
	"""
	source is a method,like source(list,textname,valuename),and the list like [{'text':'name','value':'abc'},..]
	"""
	self.field = field
	self.title = title
	self.width = width
	self.align = align
	self.control = control
	self.easyclass=easyclass
	self.source = None
	self.formatter = formatter


    def __repr__(self):
	vals = self.__dict__
	keys = [item for item in vals if item not in ('easyclass','control',"source","formatter",) ]	
	strList = []
	
	if vals['control'] == 'text':
	    strList.append("<input ")
	    strList.append(str.format("type='{0}'",'text'))
	elif vals['control'] == 'select':
	    strList.append("<select ")	   

	strList.extend(str.format("id='{0}'",vals['field']))	
	strList.extend( [str.format("{0}='{1}'",key,self.__dict__[key]) for key in keys] )

	if vals['control'] == 'text':
	    strList.append(" />")
	elif vals['control'] == 'select':
	    strList.append(">")
	    #if vals['source'] :	
	    strList.append("</select>")	
	
	return " ".join(strList)

if __name__ == "__main__":
	c = Column("name","Firtname")
	c2 = Column("authors","Choose Authors",control="select")
	print c
	print c2
