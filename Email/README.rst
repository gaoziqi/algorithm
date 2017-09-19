即用即弃型邮箱注册
====================
使用示例：
 | email = Email() 构造邮箱类
 | email = Email(proxy={}) 设置代理IP，默认值{}
 | email = Email(timeout=80) 设置请求的最大延迟，默认值60
 | email = Email(obj='bccto') 设置邮箱类型，目前只支持bccto
 | mailbox = email.register() 注册邮箱，成功返回邮箱名称，失败返回False
 | mails = email.getMails() 获取当前注册邮箱内所有邮件，返回list
 | content = email.getContent(mails[0]) 解析邮件内容，返回字符串

完成日期 2017.09.19
