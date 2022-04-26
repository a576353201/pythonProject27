import os
# from Tkinter import Image
import time
import requests
import cssselect
from bs4 import BeautifulSoup


import http.cookiejar as cookielib
from bs4 import BeautifulSoup
from lxml import etree

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")
def gethtml(url0,head):
    i = 0
    while i < 5:
        try:
            html = requests.get(url = url0, headers = head,timeout = (10, 20))
            repeat = 0
            while (html.status_code != 200):  # 错误响应码重试
                print('error: ', html.status_code)
                time.sleep(20 + repeat * 5)
                if (repeat < 5):
                    repeat += 1
                html = requests.get(url = url0, headers = head,timeout = (10, 20))
            return html
        except requests.exceptions.RequestException:
            print('超时重试次数: ', i + 1)
            time.sleep(1)
            i += 1


def get_captcha():
    #获取验证码图片所在的url
    r = session.get('http://www.dedelou.com/wp-login.php', headers=headers)
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
    url = "http://www.dedelou.com/yonghuxinxi"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 260:
        return True
    else:
        return False


def login(secret, account):
    post_url = 'https://www.zzmzz.net/wp-login.php'
    postdata = {
        'pwd': account,
        'log': secret,
        # 'rememberme': 'true',
        # 'redirect_to': 'http://www.dedelou.com/wp-admin ',
        # 'testcookie': 1,
        # 'wp-submit': '登录',

    }
    try:
        # postdata["zy_security_code"] = get_captcha()

        # 不需要验证码直接登录成功
        # login_page = session.post(post_url, data=postdata, headers=headers)
        # login_code = login_page.text
        url="https://www.zzmzz.net/yuanma"
        req = gethtml(url, headers)
        html = etree.HTML(req.text)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, 'html.parser')  # 对返回的结果进行解析

        type_link0 = html.xpath('//*[@id="ceotheme"]/div[1]/section[3]/div[1]/div[1]/div/div[2]/div/a')  # 排除上级
        type_link1 = html.xpath('/html/body/div[1]/section[3]/div[1]/div[1]/div/div[2]/div/a')  # 排除上级
        href = html.xpath('/html/body/div[1]/section[3]/div[1]/div[1]/div/div[2]/div/a/@href')  # 排除上级
        zreq = gethtml(href[0], headers)
        zhtml = etree.HTML(zreq.text)
        zsoup = BeautifulSoup(zreq.text, 'html.parser')  # 对返回的结果进行解析

        zhtml_text = zsoup.select_one('.single-content')  # 排除上级


        span = html.cssselect('.card-title-desc> a')
        textlist = soup.select('.card-title-desc> a')
        imgpic = html.xpath('//*[@id="ceotheme"]/div[1]/section[3]/div[1]/div[1]/div/div[1]/a/img')
        textlist1 = html.select('#ceotheme > div.ceo-background-muted.site.ceo-zz-background > section.ceo-container > div.ceo-grid-medium.ceo-grid > div:nth-child(1) > div > div.ceo-padding-remove > div > a')

        # soup = BeautifulSoup(login_code, 'html.parser')
        # login_error = soup.find("div", {'id': 'login_error'}).text
        # print(login_error)
        # print(login_code)
    except:
        pass
    session.cookies.save()

    try:
        session.cookies.load(ignore_discard=True)
    except:
        print("Cookie 未能加载")


if __name__ == '__main__':
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    headers = {
        "Host": "www.zzmzz.net",
        "Origin": "https://www.zzmzz.net/",
        # "Referer": "http://www.dedelou.com/wp-login.php",
        # 'User-Agent': agent,
        # 'Cookie': '__yjs_duid=1_8093628660b84177d622b8f0296a2bd11625670399617; PHPSESSID=tal00p3npqo9tq7aqc0dp4m49b; wordpress_test_cookie=WP%20Cookie%20check; Hm_lvt_8d69b728ad67b34c6d5d49c1c3bff604=1625670432; cao_notice_cookie=1; Hm_lpvt_8d69b728ad67b34c6d5d49c1c3bff604=1625671866'

    }
    if isLogin():
        print('您已经登录')
    else:
        login('a1908048813', 'ydff2018')






