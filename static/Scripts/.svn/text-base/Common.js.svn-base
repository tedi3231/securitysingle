/// <reference path="./jquery-1.6.2.js">
/// <reference path="../Script/Lib/jquery-easyui-1.2.4/jquery.easyui.min.js">
/// <reference path="./jquery.easyui.validate.unobtrusive.js">
/*************************************jQuery功能扩充************************************************************/
$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    $('input[disabled]', $(this)).each(function () {
        if ($(this).attr("Name"))
            o[$(this).attr("Name")] = $(this).val();
    });
    return o;
};
/***********************************字符串功能扩充****************************************************************/
String.prototype.slice = function (start, end, step) {
    end = end || this.length;
    if (end < 0) end = this.length + end;
    if (end < start) end = start;
    if (step && typeof step == "number") {
        var length = parseInt((end - start) / step) + ((end - start) % step ? 1 : 0);
        var result = [];
        for (var i = 0; i < length; i++) {
            result.push(this.substring(start + i * step, step * (i + 1) > end ? end : step * (i + 1)));
        }
        return result;
    }
    else
        return this.substring(start, end);
}
String.prototype.insert = function (step, separator, start, end) {
    var array = this.slice(start || 0, end || this.length, step || 1);
    return array.join(separator || ',');
}
Array.prototype.contain = function (element) {
    return this.indexOf(element) != -1;
}
Array.prototype.getComboText = function (value) {
    if (typeof value == 'object' || !value)
        return value;
    var values = value.toString().split(',');
    var text = [];
    for (var j = 0; j < values.length; j++) {
        for (var i = 0; i < this.length; i++) {
            if (this[i].Value == values[j]) {
                text.push(this[i].Text);
                continue;
            };
        }
    }
    return text.join(',');
}
window.location.params = function () {
    var param = {};
    var params = this.search.replace("?", "").split("&");
    for (var i = 0; i < params.length; i++) {
        param[params[i].split('=')[0]] = params[i].split('=')[1];
    }
    return param;
}
/**********************************jquery-easyui功能扩充**************************************************************/
$.extend($.fn.validatebox.defaults.rules, {
    minlength: {
        validator: function (value, param) {
            return value.length >= param[0];
        },
        message: '请至少输入 {0} 个字符.'
    },
    maxlength: {
        validator: function (value, param) {
            return value.length <= param[0];
        },
        message: '你最多只能输入 {0} 个字符。'
    },
    regex: {
        validator: function (value, param) {
            match = new RegExp(param[0]).exec(value)
            return (match && (match.index === 0) && (match[0].length === value.length));
        },
        message: '请输入符合条件字符串。'
    },
    equalTo: {
        validator: function (value, param) {
            return value == $('#' + param[0]).val();
        },
        message: '请输入同字段 {0} 一样的值'
    }
});
function parseEvent(attributes) {
    var result = {};
    for (var i = 0; i < attributes.length; i++) {
        if (attributes[i].name.substring(0, 2) == "on" && attributes[i].value) {
            result[attributes[i].name] = eval(attributes[i].value);
        }
    }
    return result;
}
$.fn.combobox.parseOptions = function (_4e) {
    var t = $(_4e);
    var option = $.extend({}, $.fn.combo.parseOptions(_4e), { valueField: t.attr("valueField"), textField: t.attr("textField"), mode: t.attr("mode"), method: (t.attr("method") ? t.attr("method") : undefined), url: t.attr("url"), onSelect: (t.attr("onSelect") ? eval('(' + t.attr("onSelect") + ')') : undefined) });
    return option;
};
$.fn.combobox.defaults.textField = "Text";
$.fn.combobox.defaults.valueField = "Value";
$.fn.combobox.defaults.width = 202;

$.fn.datebox.defaults.width = 202;

$.fn.datagrid.parseOptions = function (_1ab) {
    var t = $(_1ab);
    var options = $.extend({}, $.fn.panel.parseOptions(_1ab), { fitColumns: (t.attr("fitColumns") ? t.attr("fitColumns") == "true" : undefined), striped: (t.attr("striped") ? t.attr("striped") == "true" : undefined), nowrap: (t.attr("nowrap") ? t.attr("nowrap") == "true" : undefined), rownumbers: (t.attr("rownumbers") ? t.attr("rownumbers") == "true" : undefined), singleSelect: (t.attr("singleSelect") ? t.attr("singleSelect") == "true" : undefined), pagination: (t.attr("pagination") ? t.attr("pagination") == "true" : undefined), pageSize: (t.attr("pageSize") ? parseInt(t.attr("pageSize")) : undefined), pageList: (t.attr("pageList") ? eval(t.attr("pageList")) : undefined), remoteSort: (t.attr("remoteSort") ? t.attr("remoteSort") == "true" : undefined), sortName: t.attr("sortName"), sortOrder: t.attr("sortOrder"), showHeader: (t.attr("showHeader") ? t.attr("showHeader") == "true" : undefined), showFooter: (t.attr("showFooter") ? t.attr("showFooter") == "true" : undefined), scrollbarSize: (t.attr("scrollbarSize") ? parseInt(t.attr("scrollbarSize")) : undefined), loadMsg: (t.attr("loadMsg") != undefined ? t.attr("loadMsg") : undefined), idField: t.attr("idField"), toolbar: t.attr("toolbar"), url: t.attr("url"), rowStyler: (t.attr("rowStyler") ? eval('(' + t.attr("rowStyler") + ')') : undefined), onSelect: (t.attr("onSelect") ? eval('(' + t.attr("onSelect") + ')') : undefined), onLoadSuccess: (t.attr("onLoadSuccess") ? eval('(' + t.attr("onLoadSuccess") + ')') : undefined), onDblClickRow: (t.attr("onDblClickRow") ? eval('(' + t.attr("onDblClickRow") + ')') : undefined), onRowContextMenu: (t.attr("onRowContextMenu") ? eval('(' + t.attr("onRowContextMenu") + ')') : undefined), onHeaderContextMenu: (t.attr("onHeaderContextMenu") ? eval('(' + t.attr("onHeaderContextMenu") + ')') : undefined) });
    return options;
};

$.fn.datagrid.defaults.editors.combobox.getValue = function (editor) {
    var $editor = $(editor);
    var opt = $editor.combobox('options');
    return $editor.combobox("getValues").join(opt.separator);
}
$.fn.datagrid.defaults.editors.combobox.setValue = function (editor, value) {
    var $editor = $(editor);
    value = value || '';
    var opt = $editor.combobox('options');
    if (!opt.multiple)
        $editor.combobox("setValue", value)
    else {
        if (value) value = value.split(opt.separator);
        $editor.combobox("setValues", value);
    }
}
$.fn.numberbox.defaults.precision = 2;
$.fn.easyuiparse = function () {
    $.parser.parse(this);
    return this;
}
if ($.messager) {
    $.messager.defaults.ok = '是';
    $.messager.defaults.cancel = '否';
}
$.fn.formsumbit = function (callback) {
    var $form = this;
    var opt = $form.data('form');
    if (opt) {
        if (!opt.options.onSubmit())
            return;
    }
    if (!$form.form('validate'))
        return;
    var param = $form.serializeObject();

    $.messager.progress({
        title: '请稍后',
        msg: '数据提交中...'
    });
    $.post($form.attr('action'), param, function (data) {
        $.messager.progress('close');
        if (data.Result == 'success') {
            $.messager.alert('恭喜你', data.Message, 'info');
            if (callback) {
                callback(data);
            }
        }
        else
            $.messager.alert('出错了', data.Message, 'error');
    });
}

function onComboboxSelect(value, $elem, lowername) {
    $.getJSON("/Home/GetList?listname=" + lowername + "&parentvalue=" + value.Value, null, function (data) {
        $elem.combobox('loadData', data);
        $elem.combobox('select','');
    });
}

$.ajaxSetup({ cache: false });
/**********************************datagrid功能扩充**************************************************************/

function getdatagrid(element) {
    return $(element).parents("div.datagrid-view").find('>table');
}
function postcallback($grid, data) {
    if (data.Result == 'success') {
        $.messager.alert('恭喜', data.Message, 'info');
        $grid.datagrid('reload');
    }
    else {
        $.messager.alert('错误', data.Message, 'error');
    }
}
function confirmpost($grid, url, text) {
    $.messager.confirm('确认', '你确定要' + text + '么?', function (b) {
        if (b) {
            $.messager.progress({
                title: '请耐心等待',
                msg: '正在努力为你处理数据...'
            });
            $.post(url, null, function (data) {
                $.messager.progress('close');
                postcallback($grid, data);
            });
        }
    });
}
function postadd(gridid, url, data) {
    $.messager.progress({ title: "请稍后", msg: "数据处理中......" });
    $.post(url, data, function (result) { $.messager.progress('close'); postcallback($('#' + gridid), result) });
}
$.extend($.fn.datagrid.methods, {
    renderaction: function (datagrid, param) {
        var $grid = $(datagrid);
        var records = $grid.datagrid('getSelections');
        var guid = [];
        var needselect = param.needselect == undefined ? true : param.needselect;
        var openwindow = param.openwindow == undefined ? true : param.openwindow;
        if (!records.length && needselect) {
            $.messager.alert('警告', '你必须选中一行才能继续操作!', 'warning');
            return;
        }
        for (var i = 0; i < records.length; i++) {
            guid.push(records[i].Id);
        }
        var url = param.url;
        if (guid.length && needselect)
            url = url + "?id=" + guid.join(',');
        if (!openwindow) {
            confirmpost($grid, url, param.title);
        }
        else {
            var $action = $('#op_window');
            var option = { title: param.title, width: 900, height: param.height || 550, collapsible: true, maximizable: true,
                minimizable: false, modal: true,
                onClose: function () { $('#op_window_data').empty(); },
                buttons: [
                { text: '提交', iconCls: 'icon-save',
                    handler: function () {
                        $('form', $action).formsumbit(function (data) { if (!url.split('/').contain('Create')) $action.dialog('close'); $grid.datagrid('reload'); });
                    }
                },
                { text: '重置', iconCls: 'icon-undo',
                    handler: function () {
                        $('form', $action)[0].reset();
                    }
                },
                { text: '关闭', iconCls: 'icon-cancel',
                    handler: function () {
                        $action.dialog('close');
                    }
                }]
            };

            if (!$action.length) {
                $action = $('<div id="op_window" style="position:relative;left:0;top:0;"></div>').appendTo($('body'));
                $('<div id="op_window_wait" style="width:98%;height:96%;display:none;background:url(../../Content/images/ajax-loader.gif) no-repeat center center;"></div>').appendTo($action);
                $('<div style="margin:5px;width:98%;padding:5px;float:left;" id="op_window_data"></div>').appendTo($action);
            }
            $action.dialog(option);
            $('#op_window_wait').show();
            $('#op_window_data').hide();
            $('#op_window_data').load(url, null, function () { $('#op_window_wait').hide(); $('#op_window_data').show().easyuiparse().unobtrusiveparse(); });
        }
    }
});
function renewmenu(menu, disitems) {
    $(menu).children().each(function () { $(menu).menu('enableItem', this) });
    if (!disitems)
        return;
    $.each(disitems.split(','), function () {
        var text = this.split(':')[0];
        var item = $(menu).menu('findItem', text);
        if (item == null) return;
        if (this.indexOf(':') > 0) {
            var param = this.split(':')[1];
            $(item.target).attr('param', param);
        }
        else
            $(menu).menu('disableItem', item.target);
    });
}
function getSelections(gridid, noalert) {
    var records = $('#' + gridid).datagrid('getSelections');
    var guid = [];
    if (records.length == 0) {
        if (!noalert)
            $.messager.alert('警告', '你还没有选择数据，不能执行本操作!', 'warning');
        return;
    }
    else {
        for (var i = 0; i < records.length; i++) {
            guid.push(records[i].Id);
        }
    }
    return guid;
}
/**************************************************************************自定义插件**********************************************************/
function openselect(controller, action, title, elename, containerid) {
    var $container = $('#' + containerid);
    var text = $container.attr("textfield");
    var value = $container.attr("valuefield");
    var extrattr = [];
    var attribute = $('input[name=' + elename + ']', $container)[0].attributes;
    for (var i = 0; i < attribute.length; i++) {
        switch (attribute[i].name) {
            case "type":
            case "name":
            case "value": break;
            default: extrattr.push(attribute[i].name + '=' + attribute[i].value); break;
        }
    }
    var view = new Date().getTime();
    var url = '/' + controller + '/' + action + '?GridId=grid' + view;
    if (extrattr.length)
        url += '&' + extrattr.join('&');
    var option = { title: title, width: 900, height: 600, collapsible: true, maximizable: true,
        minimizable: false, modal: true, onClose: function () { $action.parent().remove(); }
    }
    var $action = $('#' + view);
    var $actiondata = $('#' + view + '_data');
    if (!$action.length) {
        $action = $('<div id="' + view + '" style="position:relative;left:0;top:0;"></div>').appendTo($('body'));
        $actiondata = $('<div style="margin:5px;width:98%;padding:5px;float:left;" id="' + view + '_data"></div>').appendTo($action);
    }
    $action.dialog(option);
    $actiondata.hide();
    var messageclosed = false;
    $.messager.progress({
        title: '请耐心等待',
        msg: '正在努力为你加载页面...'
    });
    setTimeout(function () { if (!messageclosed) $.messager.progress('close') }, 5000);
    $actiondata.load(url, null, function () {
        $.messager.progress('close');
        messageclosed = true;
        $actiondata.show().easyuiparse().unobtrusiveparse();
        var option = $('#grid' + view, $actiondata).datagrid('options');
        option.onSelect = function (index, data) {
            $action.dialog('close');
            $('#' + elename, $container).val(data[text]).trigger('change', { Value: data[value], Text: data[text] });
            $('input[name=' + elename + ']', $container).val(data[value]);
        };
    });
}