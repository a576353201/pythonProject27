import urllib.request, urllib.parse
import http.cookiejar

get_url = 'https://www.zzmzz.net/wp-content/themes/ceomax/ceoshop/erphpdown/download.php?postid=55193&key=1&index='
cookie_filename = 'cookie.txt'
cookie_aff = http.cookiejar.MozillaCookieJar(cookie_filename)
cookie_aff.load(cookie_filename,ignore_discard=True,ignore_expires=True)

handler = urllib.request.HTTPCookieProcessor(cookie_aff)
opener = urllib.request.build_opener(handler)
#使用cookie登陆get_url
get_request = urllib.request.Request(get_url)
get_response = opener.open(get_request)
print(get_response.read().decode())