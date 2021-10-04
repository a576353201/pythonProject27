import os
# from Tkinter import Image
import requests
import http.cookiejar as cookielib
from bs4 import BeautifulSoup

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_captcha():
    #获取验证码图片所在的url
    r = session.get('https://www.cgzyw.com/wp-login.php', headers=headers)
    # soup = BeautifulSoup(r.text, "lxml")
    soup = BeautifulSoup(r.text, 'html.parser')
    captcha_url = soup.find("img", {'class': 'bk'})["src"]
    # 获取验证码图片
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # try:
    #     # im = Image.open('captcha.jpg')
    #     # im.show()
    #     # im.close()
    # except:
    #     print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha

def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.cgzyw.com/yonghuxinxi"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 260:
        return True
    else:
        return False


def login(secret, account):
    post_url = 'http://www.cgzyw.com/wp-login.php'
    postdata = {
        'pwd': secret,
        'log': account,
        'rememberme': 'true',
        'redirect_to': 'https://www.cgzyw.com/yonghuxinxi',
        'testcookie': 1,

    }
    try:
        postdata["zy_security_code"] = get_captcha()

        # 不需要验证码直接登录成功
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.text

        soup = BeautifulSoup(login_code, 'html.parser')
        login_error = soup.find("div", {'id': 'login_error'}).text
        print(login_error)
        # print(login_code)
    except:
        pass
    session.cookies.save()

    try:
        session.cookies.load(ignore_discard=True)
    except:
        print("Cookie 未能加载")


if __name__ == '__main__':
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {
        "Host": "www.cgzyw.com",
        "Origin": "https://www.cgzyw.com",
        "Referer": "https://www.cgzyw.com/wp-login.php",
        'User-Agent': agent,
        'Cookie': '__yjs_duid=1_8093628660b84177d622b8f0296a2bd11625670399617; PHPSESSID=tal00p3npqo9tq7aqc0dp4m49b; wordpress_test_cookie=WP%20Cookie%20check; Hm_lvt_8d69b728ad67b34c6d5d49c1c3bff604=1625670432; cao_notice_cookie=1; Hm_lpvt_8d69b728ad67b34c6d5d49c1c3bff604=1625671866'

    }
    if isLogin():
        print('您已经登录')
    else:
        login('#ydff2020','a576353201')






