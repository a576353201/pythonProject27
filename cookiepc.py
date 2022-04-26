import urllib.error, urllib.request, urllib.parse
import http.cookiejar

LOGIN_URL = 'https://www.zzmzz.net/wp-login.php'
#get_url为使用cookie所登陆的网址，该网址必须先登录才可
get_url = 'https://www.zzmzz.net/wp-content/themes/ceomax/ceoshop/erphpdown/download.php?postid=55195&iframe=1'
values = {'log':'a1908048813','pwd':'ydff2018','rememberme':'forever','testcookie':'1'}
postdata = urllib.parse.urlencode(values).encode()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
headers = {'User-Agent':user_agent, 'Connection':'keep-alive'}
#将cookie保存在本地，并命名为cookie.txt
cookie_filename = 'cookie.txt'
cookie_aff = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie_aff)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(LOGIN_URL, postdata, headers)
try:
    response = opener.open(request)
except urllib.error.URLError as e:
    print(e.reason)

cookie_aff.save(ignore_discard=True, ignore_expires=True)

for item in cookie_aff:
    print('Name ='+ item.name)
    print('Value ='+ item.value)
#使用cookie登陆get_url
get_request = urllib.request.Request(get_url,headers=headers)
get_response = opener.open(get_request)
print(get_response.read().decode())