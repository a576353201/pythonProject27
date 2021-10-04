#encoding: utf-8
import gzip
import urllib2
import cookielib
import urllib
import re
import sys

from urllib3.packages.six import BytesIO

'''模拟登录'''
reload(sys)
sys.setdefaultencoding("utf-8")
# 防止中文报错
CaptchaUrl = "https://ssz44444.com/?c=auth&a=get_pic_code"
PostUrl = "https://ssz44444.com/?c=lottery_user&a=login"
# 验证码地址和post地址
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
# 将cookies绑定到一个opener cookie由cookielib自动管理
username = 'abc889977'
password = 'abc456'
# 用户名和密码
picture = opener.open(CaptchaUrl).read()
# 用openr访问验证码地址,获取cookie
local = open('f:/image.jpg', 'wb')
local.write(picture)
local.close()
# 保存验证码到本地
piccode = raw_input('输入验证码： ')
# 打开保存的验证码图片 输入
postData = {

'username': username,
'passwd': password,
'go':	"/pc.php?c=pc",
'piccode':	piccode,

}
# 根据抓包信息 构造表单
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Connection': 'keep-alive',
    'Cookie': 'm_200000036_pid=889; m_last_login=1625628780',
    'Referer': 'https://ssz44444.com/',
    'Origin': 'https://ssz44444.com',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
}
# 根据抓包信息 构造headers
data = urllib.urlencode(postData)
# 生成post数据 ?key1=value1&key2=value2的形式
request = urllib2.Request(PostUrl, data, headers)
response = opener.open(request)


# response = gzip.GzipFile(fileobj=response)
result = response.read().decode('utf-8')
# print result


# request1 = urllib2.Request(PostUrl, data, headers)
# 构造request请求
# try:
#  response = opener.open(request)
# result = response.read().decode('utf-8')
# # 由于该网页是gb2312的编码，所以需要解码
# print result
# # 打印登录后的页面
#
# except urllib2.HTTPError,e:
# print e.code
# 利用之前存有cookie的opener登录页面