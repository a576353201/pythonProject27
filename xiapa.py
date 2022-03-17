import requests
from lxml import etree
import pandas as pd
from pandas import DataFrame
import mysql.connector
import time
import sys
from babel.numbers import format_currency
import re


# https://shopee.tw/api/v2/item/get_ratings?flag=1&itemid=4058929120&limit=3&offset=0&shopid=322104456
def gethtml(url0, head):
    i = 0
    while i < 5:
        try:
            # url0='https://shopee.tw/api/v4/item/get?itemid=13518133767&shopid=527105502'
            html = requests.get(url=url0, headers=head, timeout=(10, 20))
            repeat = 0
            while (html.status_code != 200):  # 错误响应码重试
                print('error: ', html.status_code)
                time.sleep(20 + repeat * 5)
                if (repeat < 5):
                    repeat += 1
                html = requests.get(url=url0, headers=head, timeout=(10, 20))
            return html
        except requests.exceptions.RequestException:
            print('超时重试次数: ', i + 1)
            time.sleep(1)
            i += 1
    raise Exception()


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="tE9MKDewI5hfA5gT",
    # database="shopry"
    database="shopt"
)
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="wwwhuanl_shop",
#   passwd="m]]u_xjGjxg",
#   database="wwwhuanl_shop",
# charset="utf8mb4"
# )
mycursor = mydb.cursor()

# v2 = sys.argv[2]

v1 = '少女内衣'
v2 = 1234
# v1 = sys.argv[1]
#
# v2 = sys.argv[2]

# v1 = "rule"
#
# f = open('C:\\Users\\Administrator\\PycharmProjects\\pythonProject2\\1.txt', 'w')
# print('OKOKOK')
# f.write(v1)
# f.close()

hea = {
    'authority': 'shopee.tw',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36',
    'x-api-source': 'rweb',
    'x-shopee-language': 'zh-Hant',
    'x-requested-with': 'XMLHttpRequest',
    'af-ac-enc-dat': 'AAEAAAF8Of3T9gAAAAABdAAAAAAAAAABb1k6wrTNVP1NNdM9as916jiA4GT9LklCTUQXZjpaUBczgqAc4USplDuN/YARvSyI4PMWW4reWJniFIjkEuTY0HwJfJIWbi61tK0ogR7OSA41QtazWx4qJUrBRJo8AiDJm87UwQ9G4o8zdq5cN6r/Sl3mQOFjPZfJA8K+zqyIbnOkhHywiCkbSjkq/KdgR9INf5yoWcIPM3p30/HmKjL7OmHDFgfD1IdFP3HPZzFhMjaQY42xBkd55pTEAAaS1gBswEAL1erZ7M6Jg13jf29RcLXglTHaF3xtRLGCtKbkBw36puWUDCNQnWs1gQSFkyS0X39B0QLRR9GNS7GuzO1Rvk9eMQYZbLcMxVW6RkoOz7aUQn2Uh3c9QjNqh1fl4mSsl/82EyfDx/bVRcPaaRvYmzh+DKHI6ZY7B6MOjsq0ZXu9acps7FvnW3xcJWyKahAWl/82EyfDx/bVRcPaaRvYm8qgXl6Fao3/VUKjEYKkOU8n67NdgEQvAnHJfCuJRB9f',
    'if-none-match-': '55b03-b10a87df23525ef937a592ce52210527',
    'sec-ch-ua-platform': '"Android"',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://shopee.tw/iPhone13-%E8%98%8B%E6%9E%9C13-%E8%98%8B%E6%9E%9C%E9%8F%A1%E9%A0%AD%E8%86%9C%E8%98%8B%E6%9E%9C12Promax%E9%8F%A1%E9%A0%AD%E8%86%9CiPhone13%E9%88%A6%E5%90%88%E9%87%91%E5%85%A8%E8%A6%86%E8%93%8B12%E7%82%AB%E5%BD%A9%E9%96%83%E9%91%BDip11%E9%91%BD%E7%9F%B3%E8%B6%85%E8%96%84-i.527105502.13518133767?position=0',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'REC_T_ID=a3f6fce2-1fb7-11ec-b032-d09466041c6b; _gcl_au=1.1.1214922703.1632768612; SPC_IA=-1; SPC_F=ouxdxbiZb1POSiYlwddIYkbpGRARJ6c1; _fbp=fb.1.1632768615123.478588372; __BWfp=c1632768616136x877733d29; G_ENABLED_IDPS=google; SPC_ST=".ZHFjUUxnZThqazQxWlNtTtjZRK5C9MGAquxANTWr8XzWiZPSwggdoILVt2KP3/74sZfGt9umBsFx6NRD4+4YiOzYhUH07Mlmzl66u2+KoMG2I1aWqCYxoJd5P8LDYHvWi3ha72knkCwZWUSJONJzfU1b5LWxqcYx4n/zU3BYuYDcstXtShNtwZs14rNVytl6p2BD5qSySClsdjzGabRVEg=="; SPC_U=549058135; SPC_CLIENTID=b3V4ZHhiaVpiMVBPqbfoflcamgckbsqn; SPC_EC=WGtFbFFzcUF1aHQ1WnF4cQfEz1lTMxUOp6PqFOqburpZHXKO3RGyyb98UYrGix391nh+puytD5dpyvCQe/yQJ8T1Oa5ATAip+0zwexzMrFvo6kYJ1k/D5Nf7LG7jaTBeuLhOHfWpUHhteCuo1NGHBTlhG6ezWNc6oe/wYBlUjtQ=; SPC_SI=bfftoctw1.767ox9zbeUisgs9oue9n2bOHfrWoJ5tw; csrftoken=6P4FcvrozTt8J8ExY7c5MY6qaBp2kd5F; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.2.423118293.1632768616; _gid=GA1.2.1160741941.1633060057; cto_bundle=ymHcg19Lc0cyV1YxbFc3ZzlFamp5TUg3M2hHRnVPViUyRnp1eVVsTWQ5eSUyRk1HdjFjZVd0QW5aRXBvVjclMkJ4Wk9mVmVPcTBCOUNNb3V3OGFOdURWYzlhM2xSN3BHQzRqWFdzY0wxTEpYUm1kbWNEcEt6WjRwaWtBUnliZEpJSWtLemgxb2FmV0JpeTZ3RXhua29TcW9scHNHTVhMYnclM0QlM0Q; SPC_T_IV="vuT9UrdcUCYEsqoEaTnlsw=="; SPC_T_ID="z9BtKth6qKiQ4Ya5JIjVyKsMN8Ev/eV+dJtP9znV95LC8yLPIPKPoDOylSZgz8p1jYV5soEEn3Jjq7c0T/ZTF3jzuyp+WXYOKN1vC7fUiXU="; SPC_R_T_ID=z9BtKth6qKiQ4Ya5JIjVyKsMN8Ev/eV+dJtP9znV95LC8yLPIPKPoDOylSZgz8p1jYV5soEEn3Jjq7c0T/ZTF3jzuyp+WXYOKN1vC7fUiXU=; SPC_R_T_IV=vuT9UrdcUCYEsqoEaTnlsw==; SPC_T_ID=z9BtKth6qKiQ4Ya5JIjVyKsMN8Ev/eV+dJtP9znV95LC8yLPIPKPoDOylSZgz8p1jYV5soEEn3Jjq7c0T/ZTF3jzuyp+WXYOKN1vC7fUiXU=; SPC_T_IV=vuT9UrdcUCYEsqoEaTnlsw==; _dc_gtm_UA-61915057-6=1; _ga_RPSBE3TQZZ=GS1.1.1633060048.6.1.1633060506.18',
}

df = DataFrame({
    '类别': {},
    '排名': {},
    '照片链接': {},
    '商品链接': {},
    '标题': {},
    '星级': {},
    '评论数': {},
    '低价格': {},
    '高价格': {},

})

qstr = v1
qstr1 = 'pen5'
path = 'pm.csv'
# df_type = list(pd.read_csv(path)['类别'])
# df_link = list(pd.read_csv(path)['链接'])

# if 3 > 2:
#     qstr = v1
#     print(qstr)
#     f = open('C:\\Users\\Administrator\\PycharmProjects\\pythonProject2\\1.txt', 'w')
#     print('OKOKOK')
#     f.write("qstr")
#     f.close()


mycursor.execute("select name,id from fa_wanlshop_category where pid!=0 and image!='2' order by id asc")

fldata = mycursor.fetchall()
 ## 空列表
for row in fldata:
    time.sleep(2)
    qstr = row[0]
    v2 = row[1]
    df_link = []
    df_linkstr = 'https://shopee.sg/api/v4/search/search_items?by=relevancy&keyword=%s&limit=20&newest=20&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2' % (

        #df_linkstr = 'https://my.xiapibuy.com/api/v4/search/search_items?by=relevancy&keyword=%s&limit=20&newest=20&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2' % (

        str(qstr))
    # df_linkstr='https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword=布質尿布&limit=20&newest=20&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'
    df_link.append(df_linkstr)
    for link in range(0, len(df_link)):
        time.sleep(2)
        for j in range(0, 1):
            url0 = df_link[link]
            url1 = url0.split('ref=', 2)[0]
            url2 = "ref=zg_bs_pg_%s?_encoding=UTF8&pg=%s" % (str(j), str(j))
            url = url1
            print(url)
            req = gethtml(url, hea)
            html = req.json()

            # print(html)
            # time.sleep(10)
            try:
                for i in range(len(html['items'])):
                    z = i + (j - 1) * 50 + link * 100  # 调整序号
                    title = html['items'][i]['item_basic']['name']
                    image = html['items'][i]['item_basic']['image']
                    images = html['items'][i]['item_basic']['images']
                    image = "https://cf.shopee.sg/file/" + image
                    stock = html['items'][i]['item_basic']['stock']
                    price = html['items'][i]['item_basic']['price']
                    category_id = v2
                    freight_id = 1
                    shop_id = 1
                    brand_id = 1
                    grounding = 1
                    specs = 'single'
                    distribution = 'false'
                    activity = 'false'
                    views = 0
                    description = ''
                    proid = str(html['items'][i]['itemid']) + ',' + str(html['items'][i]['shopid'])
                    purl = 'https://shopee.sg/api/v2/item/get?itemid=%s&shopid=%s' % (
                        str(html['items'][i]['itemid']), str(html['items'][i]['shopid']));
                    preq = gethtml(purl, hea)
                    pjson = preq.json()
                    pitem = pjson['item']
                    try:
                        description = pitem['description']
                    except:
                        description = '.'
                    images = ",".join(images)
                    images = "https://cf.shopee.sg/file/" + images.replace(",", ",https://cf.shopee.sg/file/")
                    # price= format_currency(price, 'USD', locale='en_US')
                    price = str(price)[:-5]

                    mycursor.execute("select * from fa_wanlshop_goods where proid='" + proid + "'")

                    data = mycursor.fetchall()
                    if (len(data) != 0):
                        continue
                    sql = 'Insert  Into `fa_wanlshop_goods` (`title`,`image`,`images`,`price`,`category_id`,`shop_id`,`brand_id`,`freight_id`,`grounding`,`specs`,`distribution`,`activity`,`views`,`content`,`proid`) Values (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    val = (
                        title, image, images, price, category_id, shop_id, brand_id, freight_id, grounding, specs,
                        distribution,
                        activity, views, description, proid)
                    print(title)
                    mycursor.execute(sql, val)
                    goodsid = mycursor.lastrowid
                    mydb.commit()
                    spu = pitem['tier_variations']
                    models = pitem['models']
                    for k in range(len(spu)):
                        spuname = spu[k]['name']
                        item = ",".join(spu[k]['options'])
                        sql = "INSERT INTO fa_wanlshop_goods_spu (name, item,goods_id) VALUES (%s, %s, %s)"
                        val = (spuname, item, goodsid)
                        # mycursor.execute(sql, val)
                        # spuid = mycursor.lastrowid
                        mydb.commit()
                    for k in range(len(models)):
                        # spuname=spu[k]['name']
                        difference = models[k]['name']
                        price = models[k]['price']
                        market_price = models[k]['price']
                        stock = models[k]['stock']
                        price = str(price)[:-5]
                        market_price = str(market_price)[:-5]
                        sn = 11
                        sql = "INSERT INTO fa_wanlshop_goods_sku (difference, price,market_price,stock,goods_id,weigh,sn) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        val = (difference, price, market_price, stock, goodsid, 1, sn)
                        # mycursor.execute(sql, val)
                        # skuid = mycursor.lastrowid
                        mydb.commit()
                    a2 = html['items'][i]['item_basic']['name']

                    headers = {
                        'authority': 'shopee.tw',
                        'pragma': 'no-cache',
                        'cache-control': 'no-cache',
                        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                        'sec-ch-ua-mobile': '?0',
                        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
                        'x-api-source': 'pc',
                        'x-shopee-language': 'zh-Hant',
                        'x-requested-with': 'XMLHttpRequest',
                        'if-none-match-': '55b03-e1952be5f7d6190f512e49e032045239',
                        'sec-ch-ua-platform': '"Windows"',
                        'accept': '*/*',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-dest': 'empty',
                        'referer': 'https://shopee.sg/product/%s/%s' % (
                            str(html['items'][i]['itemid']), str(html['items'][i]['shopid'])),
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'cookie': 'REC_T_ID=a3f6fce2-1fb7-11ec-b032-d09466041c6b; _gcl_au=1.1.1214922703.1632768612; SPC_IA=-1; SPC_F=ouxdxbiZb1POSiYlwddIYkbpGRARJ6c1; _fbp=fb.1.1632768615123.478588372; __BWfp=c1632768616136x877733d29; G_ENABLED_IDPS=google; SPC_ST=".ZHFjUUxnZThqazQxWlNtTtjZRK5C9MGAquxANTWr8XzWiZPSwggdoILVt2KP3/74sZfGt9umBsFx6NRD4+4YiOzYhUH07Mlmzl66u2+KoMG2I1aWqCYxoJd5P8LDYHvWi3ha72knkCwZWUSJONJzfU1b5LWxqcYx4n/zU3BYuYDcstXtShNtwZs14rNVytl6p2BD5qSySClsdjzGabRVEg=="; SPC_U=549058135; SPC_CLIENTID=b3V4ZHhiaVpiMVBPqbfoflcamgckbsqn; SPC_EC=WGtFbFFzcUF1aHQ1WnF4cQfEz1lTMxUOp6PqFOqburpZHXKO3RGyyb98UYrGix391nh+puytD5dpyvCQe/yQJ8T1Oa5ATAip+0zwexzMrFvo6kYJ1k/D5Nf7LG7jaTBeuLhOHfWpUHhteCuo1NGHBTlhG6ezWNc6oe/wYBlUjtQ=; SPC_SI=bfftoctw1.hzwtZdHuiHPdBwIeePYSVB2OSZf53hp0; csrftoken=oFoeA7tMkP2lRkEQFPV3usRJhtftPZfs; _gid=GA1.2.27729051.1633191977; welcomePkgShown=true; AMP_TOKEN=%24NOT_FOUND; _dc_gtm_UA-61915057-6=1; _ga=GA1.2.423118293.1632768616; SPC_T_IV="SLwdXyUnSa3QAqeLxhmuNw=="; SPC_T_ID="lr/HN/FRRt60QqkSR092UqQlaEWvjpgk6xKZu9DlmxORNvg0NtuamxzLBBwx7Sj+QUgsu6cGTl9LdUSLTyVeyVjNfRf7A2SyM680otZYltY="; SPC_R_T_ID=lr/HN/FRRt60QqkSR092UqQlaEWvjpgk6xKZu9DlmxORNvg0NtuamxzLBBwx7Sj+QUgsu6cGTl9LdUSLTyVeyVjNfRf7A2SyM680otZYltY=; SPC_R_T_IV=SLwdXyUnSa3QAqeLxhmuNw==; SPC_T_ID=lr/HN/FRRt60QqkSR092UqQlaEWvjpgk6xKZu9DlmxORNvg0NtuamxzLBBwx7Sj+QUgsu6cGTl9LdUSLTyVeyVjNfRf7A2SyM680otZYltY=; SPC_T_IV=SLwdXyUnSa3QAqeLxhmuNw==; cto_bundle=y9B1al9Lc0cyV1YxbFc3ZzlFamp5TUg3M2hHbDNNQjh6Y3pvYjBqUUk5R3Q1T0JGTHFMT1lDNFJncExWSHhIWVd2T3p3T3hSbHdvdEJDZzFtMk1laHBxTU01ajJYdkxxc1dnSk5GSlA3TVRET0d6RG4yZzFKY2t0bEVqRDNFcW5sSzlMSDlybEdKJTJCdzFUREhMY05XTWtwUEZqQSUzRCUzRA; _ga_RPSBE3TQZZ=GS1.1.1633207226.10.1.1633208232.60',
                    }

                    purl = 'https://shopee.sg/api/v2/item/get_ratings?flag=1&itemid=%s&limit=3&offset=0&shopid=%s' % (
                        str(html['items'][i]['itemid']), str(html['items'][i]['shopid']));
                    preq = gethtml(purl, headers)
                    pjson = preq.json()
                    if pjson['data']['ratings'] != None:
                        for k in range(len(pjson['data']['ratings'])):
                            user_id = 1
                            content = pjson['data']['ratings'][k]['comment']
                            shop_id = 1
                            order_id = 1
                            goods_id = goodsid
                            order_goods_id = goodsid
                            suk = pjson['data']['ratings'][k]['product_items'][0]['model_name']
                            if suk == None:
                                suk = '';
                            # print(pjson['data']['ratings'][k]['images'])
                            images = ''
                            if (isinstance(pjson['data']['ratings'][k]['images'], list)):
                                images = ",".join(pjson['data']['ratings'][k]['images'])
                                images = "https://cf.shopee.sg/file/" + images.replace(",",
                                                                                       ",https://cf.shopee.sg/file/")
                            sql = "INSERT INTO fa_wanlshop_goods_comment (user_id, content,shop_id,order_id,goods_id,order_goods_id,suk,images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                            val = (user_id, content, shop_id, order_id, goods_id, order_goods_id, suk, images)
                            # mycursor.execute(sql, val)
                            # spuid = mycursor.lastrowid
                            mydb.commit()
                        pjson = preq.json()
            except:
                d = 1









# path0 = 'd:/pm22.csv'
# df.to_csv(path0, encoding='utf-8', index=False)  # 去掉index，保留头部
