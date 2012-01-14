#coding=utf8

class Column(object):
    def __init__(self,field,title,width=100,align="left",control="input",controltype="text",
                 easyclass="",source=None,formatter=None,defaultvalue=None,show=True):
        self.field = field
        self.title = title
        self.width = width
        self.align = align
        self.control = control
        self.controltype = controltype
        self.easyclass=easyclass
        self.source = source
        self.formatter = formatter
        self.defaultvalue = defaultvalue
        self.show=show
        #print show

    def __repr__(self):
    	vals = self.__dict__
        keys = [item for item in vals if item not in ('easyclass','control','controltype',"source",
                                                      "formatter",'defaultvalue')]
        strList=[]
        if vals['control'] == 'input':
            strList.append( str.format("<input type='{0}'",vals['controltype']))
            if vals['defaultvalue']:
                strList.append(str.format("value='{0}'",vals['defaultvalue']))
        elif vals['control'] == 'select':
		    strList.append("<select ")
        strList.append(str.format("id='{0}' name='{0}'",vals['field']))
        strList.extend( [str.format("{0}='{1}'",key,self.__dict__[key]) for key in keys] )
        if vals['easyclass']:
		    strList.append(str.format("class='{0}'",vals['easyclass']))
        if vals['control'] == 'input':
		    strList.append(" />")
        elif vals['control'] == 'select':
	    	strList.append(">")
        if vals['source']:
	    	#print 'have source '
		    #print vals['source']
            rows = vals['source']['rows']
            valuename = vals['source']['valuename']
            valuetext = vals['source']['valuetext']
            for row in rows:
			    #print 'row value' + row[valuetext]
	        	strList.append(str.format("<option value='{0}' {2}>{1}</option>",row[valuename],row[valuetext],
					  "selected" if str(row[valuename])==str(vals['defaultvalue']) else ''))	
            strList.append("</select>")
        #print vals['defaultvalue']
        #print " ".join(strList)
        return " ".join(strList)


class GridData(dict):
    def __init__(self):
        self['total'] = 0
        self['rows'] = []
        self['footer'] = []
        
    def __setitem__(self, key, value):
        if not key in ('total', 'rows', 'footer'):
            raise KeyError('must be total,rows,or footer')
        dict.__setitem__(self, key, value)


if __name__ == "__main__":
	c = Column("name","Firtname")
	#c2 = Column("authors","Choose Authors",control="select")
	rows = [{"name":"pancy","title":"test1"},{"name":"tedi3231","title":"test2"}]
	d1 = {"rows":rows,"valuename":"name","valuetext":"title"}
	c3 = Column("authors","Choose Authors", control = "select",easyclass="combox",source = d1,defaultvalue='tedi3231' )
	print c
	#print c2
	print c3
