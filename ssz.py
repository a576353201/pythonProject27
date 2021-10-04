import json
import os
# from Tkinter import Image
import time

import requests
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
from selenium import webdriver
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_captcha():
    #获取验证码图片所在的url
    r = session.get('https://ssz44444.com', headers=headers)
    # soup = BeautifulSoup(r.text, "lxml")
    soup = BeautifulSoup(r.text, 'html.parser')
    captcha_url = soup.find("img", {'alt': '验证码'})["src"]
    # 获取验证码图片
    r = session.get('https://ssz44444.com'.captcha_url, headers=headers)
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
    url = "https://ssz44444.com/yonghuxinxi"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 260:
        return True
    else:
        return False


def login1(secret, account):
    post_url = 'https://ssz44444.com/?c=lottery_user&a=login'


    postData = {

        'username': account,
        'passwd': secret,
        'go': "/pc.php?c=pc",
        # 'piccode': piccode,

    }
    try:
        postData["piccode"] = get_captcha()

        # 不需要验证码直接登录成功
        login_page = session.post(post_url, data=postData, headers=headers)
        login_code = login_page.text

        soup = BeautifulSoup(login_code, 'html.parser')
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

def login(username, password):

            url = 'https://ssz44444.com/'
            # driver = webdriver.Chrome(
            #     executable_path='D:\chromedriver_win32\chromedriver.exe')
            driver = webdriver.Firefox()
            driver.get(url)
            driver.get_screenshot_as_file('yanzhengma.png')  # 截图网页保存
            # print driver.title
            name_input = driver.find_element_by_name('username')  # 找到用户名的框框
            pass_input = driver.find_element_by_name('passwd')  # 找到输入密码的框框
            yanzheng_input = driver.find_element_by_name('piccode')  # 验证码输入框
            login_button = driver.find_element_by_id('login')  # 找到登录按钮
            name_input.clear()
            name_input.send_keys(username)  # 填写用户名
            # time.sleep(0.2)
            pass_input.clear()
            pass_input.send_keys(password)  # 填写密码
            # 验证码获取
            # local方法专用，截取验证码所在的网页
            # yzm = yanzheng_local()
            yzm = input("please input the captcha\n>")
            yanzheng_input.send_keys(yzm)
            time.sleep(1.2)
            login_button.click()  # 点击登录
            time.sleep(1.2)
            ooks=driver.get_cookies()
            cookies = {}  # 换成上一步获取的Cookies
            data1=[]
            ttstr=''
            ttstr1=''

            for cookie in ooks:
                cookies.cookie['name']= cookie['value']
                cookstr = cookie['name'] + "=" + cookie['value'] + ";"
                ttstr += cookstr

            data1['sid']=cookies['m_sid']
            data1['cookies']=cookies
            b = json.dumps(data1)

            # # 刷新页面
            driver.refresh()
            # # 刷新页面
            # driver.refresh()
            headers1['Cookie']=ttstr
            r = session.post('https://www.ssz44444.com/api/user/balance',b, headers=headers1)
            dd= driver.get('https://www.ssz44444.com/api/user/balance')
            if ('login' in driver.current_url):
                print("登录成功")
                driver.close()
if __name__ == '__main__':
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    headers = {
        "Host": "ssz44444.com",
        'Referer': 'https://ssz44444.com/',
        'Origin': 'https://ssz44444.com',
        'User-Agent': agent,
        'Cookie': 'm_200000036_pid=889; m_pcode=ur779890825_6058a133e1122f25cdbe7ab13ac0'

    }

    headers1 = {
        "Host": "ssz44444.com",
        'Referer': 'https://ssz44444.com/pc/game/mspk10',
        'Origin': 'https://ssz44444.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    }
    if isLogin():
        print('您已经登录')
    else:
        login('abc889977', 'abc456')





