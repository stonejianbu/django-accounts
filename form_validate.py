"""
##  HTML表单和JavaScript检验

> form_validate.py文件主要是进行字符串的拼接和写入HTML和js文件。
> py文件包含包含四个函数（patterns, generate_html, generate_js, generate）和几个常量（HTML和js模板）;


此文件是基于**django模板语言**的，通过调用一个接口（```generate(...)```）
而同时生成表单HTML和相应javascript表单验证代码以及结合bootstrap框架。
**所以需要在base.html中导入jquery.js,bootstrap的js和css文件,这些文件在文件夹中提供**_。

目前提供了```mail,username, name, password, url, ipv4, color16, ic(身份证), qq, wx, car,number```(未提供max和min属性)等等匹配的模式，
当默认的匹配模式不符合自身需求时，可调用函数```patterns（...）```重写匹配模式。

```
注：正则匹配模式是优先于长度检查的，具体可查看变量base_js字符串中的JavaScript函数```checkInsert(...)```
注：提供的默认匹配模式并非严格讲究，只是简单参考！
```
"""
# html表单模板
form_template = """
<div class="form-group">
    <label for="{0}">{1}<span class="text-danger"> *</span></label>
    <div class="input-group">
        <div class="input-group-addon"></div>  <!-- 省略会使得input不能占据100% -->
        <input id="{0}" class="form-control" type="{2}"
        name="{0}" placeholder="{3}" minlength="{4}" maxlength="{5}" required/>
    </div>
    <span id="helpBlock" class="help-block" style="color:red;"></span>
</div>
"""

# html_template模板(进行字符串拼接)
top_html = """
<!-- 继承文件 -->
{% extends 'base.html' %}
<!-- 标题 -->
{% block title %}{% endblock title %}
{% load static %}

<!-- 头部引入文件或当前页面的css和js -->
{% block topfile %}
<script src="{% static 'js/"""

mid_html = """' %}"></script>
{% endblock topfile %}

<!-- nav -->
{% block topcontent %}
{% endblock topcontent %}

<!-- 内容 -->
{% block content %}
<div class="container">
<div class="row">
<form method="post" class="col-md-6 col-md-offset-3 col-xs-8 col-xs-offset-2">
"""

bottom_html = """
<div class="checkbox">
    <label>
      <input type="checkbox"> Check me out
    </label>
  </div>
<button type="submit" class="btn btn-default">Submit</button>
</form>
</div>
</div>
{% endblock content %}

<!-- footer -->
{% block bottomcontent %}
{% endblock bottomcontent %}

<!-- 底部引入文件或js -->
{% block bottomfile %}
{% endblock bottomfile %}
"""

# js模板文件
js_template = """
// 初始化选择器
const %s = $('#%s');
%s.blur(function(){
        checkInsert(%s, {re_pattern: %s, tip_error: '%s'})
    });
"""
# js基本模板
base_js = """
// 使用js检测用户提交信息
$(function(){
    %s
    //发送post请求时在进行检验全部提交信息的合法性
    $('#form').submit(function () {
        const verify_list = [
            // 提交时，对全部信息进行检查
            %s
        ];
        for(let status of verify_list){
            if(status !== false){
                // 如果含有验证错误则禁止表单提交
                return false
            }
        }
        return true
    })
});

// 提交信息检查, 正则匹配检验优先于长度检验，长度检验(默认最小长度为0，最大长度为200)
function checkInsert(selector, {re_pattern=null, min_limit=1, max_limit=200, tip_error=null}){
        const contentLength = selector.val().length;
        let error_status;

        // 正则匹配模式检查
        if(re_pattern != null){
            // 如果正则表达式不匹配，则提示错误信息
            // 不能将正则匹配和长度检查同等检查，否则会因为满足低需求而不能正常提示错误信息
            if(!(re_pattern.test(selector.val()))){
                error_status = true;
                selector.parent().next().html(tip_error).show();
            }else{
                error_status = false;
                selector.parent().next().html('').show();
            }
        }else{
            // 输入信息长度检查
        if(contentLength < min_limit || contentLength > max_limit){
            error_status = true;
            selector.parent().next().html(tip_error).show();
        }else{
            selector.parent().next().html('').show();
            error_status = false;
        }
        }
    return error_status
}
"""


# 匹配模式
def patterns(
        # 以下为默认的正则匹配，需要自定义则传入相应的关键字参数
        re_mail='/^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/',
        re_username='/^[a-zA-Z0-9_-]{5,20}$/',
        re_name='/^[a-zA-Z0-9_-]{5,20}$/',
        re_url='/^((https?|ftp|file):\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/',
        re_password='/^[a-zA-Z0-9_]{6,16}$/',
        re_ipv4='/^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/',
        re_color16 = '/^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$/',
        re_ic='/^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/',
        re_qq='/^[1-9][0-9]{4,10}$/',
        re_wx='/^[a-zA-Z]([-_a-zA-Z0-9]{5,19})+$/',
        re_car='/^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$/',
        re_number='/^-?//d+$/',
        re_active_code = '/^[1]\d{5}$/',
        re_phone='/^1[0-9]{10}$/',
        ):
    return {
        #  0(id/for/name) 1(label) 2(type) 3(placeholder) 4(minlength) 5(maxlength) 6(re_pattern) 7(tip_error)
        'email': ['email', '邮 箱', 'email', 'Email', 5, 30, re_mail, '提示：邮箱地址格式有误，请检查并重新输入！'],
        'username': ['username', '用户名', 'text', 'UserName', 5, 30, re_username, '提示：用户名格式有误，请检查并重新输入！'],
        'name': ['name', '收件人', 'text', '请输入真实姓名或者别名', 1, 50, re_name, '提示：收件人格式有误，请检查并重新输入！'],
        'url': ['url', 'URL地址', 'url', 'url', 1, 200, re_url, '提示：url地址格式有误，请检查并重新输入！'],
        'password': ['password', '密 码', 'password', 'PassWord', 6, 16, re_password, '提示：密码格式有误，请检查并重新输入！'],
        'origin_password': ['origin_password', '密 码', 'origin_password', 'Origin Password', 6, 16, re_password, '提示：密码格式有误，请检查并重新输入！'],
        'new_password': ['new_password', '密 码', 'new_password', 'New Password', 6, 16, re_password, '提示：密码格式有误，请检查并重新输入！'],
        'ipv4': ['ipv4', 'IPv4地址', 'text', '请输入Ipv4', 10, 20, re_ipv4, '提示：ipv4格式有误，请检查并重新输入！'],
        'color16': ['color16', '请输入十六进制rgb', 'text', '十六进制颜色', 5, 30, re_color16, '提示：16进制rgb格式有误，请检查并重新输入！'],
        'ic': ['ic', '身份证', 'text', '请输入18位身份证号码', 18, 18, re_ic, '提示：身份证格式有误，请检查并重新输入！'],
        'qq': ['qq', 'QQ号', 'text', '请输入QQ号码', 5, 11, re_qq, '提示：QQ号码格式有误，请检查并重新输入！'],
        'wx': ['wx', '微信号', 'text', '请输入微信号', 5, 50, re_wx, '提示：微信号格式有误，请检查并重新输入！'],
        'car': ['car', '车牌号', 'text', '请输入车牌号', 4, 10, re_car, '提示：车牌号格式有误，请检查并重新输入！'],
        'number': ['number', '数值', 'number', '请输入数值', 1, 20, re_number, '提示：输入的数值格式，请检查并重新输入！'],   # 数值的min, max需要调整
        'active_code': ['active_code', '激活码', 'text', '请输入邮箱激活码', 6, 6, re_active_code, '提示：输入的邮箱激活码格式有误，请重新输入！'],
        'phone': ['phone', '联系方式', 'text', '请输入手机号码', 11, 11, re_phone, '提示：输入的手机号码格式有误，请检查并重新输入！'],
    }


def generate_html(fields, patterns, html_file, js_file):
    with open(html_file, 'w+', encoding='utf-8') as f:
        form_html = []
        for field in fields:
            block = form_template.format(*(patterns[field][0:6]))
            form_html.append(block)
        html = top_html + js_file + mid_html + ''.join(form_html) + bottom_html
        f.write(html)


def generate_js(fields, patterns, js_file):
    # 进行字符拼接和写入js文件
    with open(js_file, 'w+', encoding='utf-8') as f:
        # selector_event 默认事件为blur
        selector_event = []
        submit_check = []
        for field in fields:
            nid = patterns[field][0]
            re_pattern = patterns[field][6]
            tip_error = patterns[field][7]
            selector_event_str = js_template % (nid, nid, nid, nid, re_pattern, tip_error)
            submit_check_str = "checkInsert(%s, {re_pattern: %s, tip_error: '%s'})" % (nid, re_pattern, tip_error)
            selector_event.append(selector_event_str)
            submit_check.append(submit_check_str)
        js = base_js % (''.join(selector_event), ','.join(submit_check))
        f.write(js)


def generate(fields: '[mail,username, name, url, password, ipv4, color16, ic, qq, wx, car, number, active_code, phone]', patterns, html_file, js_file):
    generate_html(fields, patterns, html_file, js_file)
    generate_js(fields, patterns, js_file)


# 生成html和js文件
if __name__ == '__main__':
    # 定义匹配模式， 如果为空则使用默认匹配模式
    re_patterns = patterns()
    # 指定类型
    fields_list = ['username', 'password', 'active_code']
    generate(fields_list, re_patterns, 'register.html', 'reset_password.js')
