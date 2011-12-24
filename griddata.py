#coding=utf8
from tornado.escape import json_encode

class GridData(dict):
    def __init__(self):
        self['total'] = 0
        self['rows'] = []
        self['footer'] = []
        
    def __setitem__(self, key, value):
        if not key in ('total', 'rows', 'footer'):
            raise KeyError('must be total,rows,or footer')
        dict.__setitem__(self, key, value)

class Column(dict):
    def __init__(self):
        pass
    
    def __init__(self, field, title, width=100, align="left",noscaler=False):
        self['field'] = field
        self['title'] = title
        self['width'] = width
        self['align'] = align
        self['noscaler'] = noscaler
        
    def __setitem__(self, key, value):
        if not key in ('field', 'title', 'width', 'align','noscaler'):
            raise KeyError('must be field,title,width,align,noscaler')
        dict.__setitem__(self, key, value)
        
    def __repr__(self):       
        sList = []
        for k in self:
            sList.append(str.format("{0}='{1}'", k, self[k]))
        return " ".join(sList)

def toGridViewHtml(tableid, url, title, columns, xsrf, width=500, height=500, pagination="true", rownumbers="true"):
    sList = [str.format("<script language='javaScript'> $(document).ready(function(){ $('#{0}').datagrid({queryParams:{'_xsrf':{1}}});}); </script>", tableid, xsrf)]    
    sList.append(str.format("<table id='{0}' url='{6}' class='easyui-datagrid' title='{1}' style='width:{2};height:{3}' pagination='{4}' rownumbers='{5}'  >",
                        tableid, title, width, height, pagination, rownumbers, url))
    sList.append('<thead><tr>')
    sList.extend([str.format("<th {0}>{1}</th>", str(item), item["title"]) for item in columns]);
    sList.append("</tr></thead>")
    sList.append('</table>')
    return ''.join(sList)
        
        
def _testColumn():
    c = Column() 
    c['field'] = 'name'
    c['title'] = 'First Name'
    c['width'] = 200
    c['align'] = 'right'
    print c     

def _testToGridViewHtml():    
    cols = [
            Column('name', 'First Name', "100", "left"),
            Column('email', 'Email', "100", "left"),
            Column('id', 'ID', "100", "left")
           ]
    print (toGridViewHtml("authors", "/authors", "All Authors", cols))
       
if __name__ == "__main__":
    #data = GridData()   
    #data['totals'] = 39    
    ##data['value']=3
    #print(json_encode(data))
    #print ('a')
    _testToGridViewHtml()    
    
