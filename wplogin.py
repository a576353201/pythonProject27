import requests
session = requests.session()

post_url = 'https://www.cgzyw.com/wp-login.php'
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
headers = {
    "Host": "www.cgzyw.com",
    "Origin":"http://www.cgzyw.com",
    "Referer":"http://www.cgzyw.com/wp-login.php",
    'User-Agent': agent
}
postdata = {
    'pwd': 'a576353201',
    'log': '#ydff2020',
    'rememberme' : 'forever',
    'redirect_to': 'http://www.cgzyw.com/wp-admin/',
    'testcookie' : 1,
}

login_page = session.post(post_url, data=postdata, headers=headers)
print(login_page.status_code)