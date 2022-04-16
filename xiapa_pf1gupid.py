import MySQLdb
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
    database="shop2"

)



#mysqli_set_charset(mydb, "utf8mb4")

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="wwwhuanl_shop",
#   passwd="m]]u_xjGjxg",
#   database="wwwhuanl_shop",
# charset="utf8mb4"
# )
mycursor = mydb.cursor()

# v2 = sys.argv[2]





v1 = "rule"
#
# f = open('C:\\Users\\Administrator\\PycharmProjects\\pythonProject2\\1.txt', 'w')
# print('OKOKOK')
# f.write(v1)
# f.close()

hea = {
    'authority': 'shopee.sg',
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
    'referer': 'https://shopee.sg/iPhone13-%E8%98%8B%E6%9E%9C13-%E8%98%8B%E6%9E%9C%E9%8F%A1%E9%A0%AD%E8%86%9C%E8%98%8B%E6%9E%9C12Promax%E9%8F%A1%E9%A0%AD%E8%86%9CiPhone13%E9%88%A6%E5%90%88%E9%87%91%E5%85%A8%E8%A6%86%E8%93%8B12%E7%82%AB%E5%BD%A9%E9%96%83%E9%91%BDip11%E9%91%BD%E7%9F%B3%E8%B6%85%E8%96%84-i.527105502.13518133767?position=0',
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


#mycursor.execute("select proid,id from fa_wanlshop_goods where id=391")
# mycursor.execute("SELECT s.goods_id, k.proid FROM fa_wanlshop_goods as k LEFT JOIN fa_wanlshop_goods_spu as s on k.id = s.goods_id GROUP BY s.goods_id where s.goods_id in(1687.1688) HAVING count(s.goods_id) > 1")
mycursor.execute("SELECT proid, id FROM fa_wanlshop_goods where id in(1687,1686,1688)")

fldata = mycursor.fetchall()
## 空列表
for row in fldata:
    proid=row[0]
    proid=proid.split(",")
    # proid=proid.split(",")
    mycursor.execute('SELECT difference FROM fa_wanlshop_goods_sku where difference  like  \'%,%\' and goods_id='+str(row[1]));

    fldata1 = mycursor.fetchall()

    if(len(fldata1)):
        continue


    purl = 'https://shopee.sg/api/v4/item/get?itemid=%s&shopid=%s' % (
        str(proid[0]), str(proid[1]));
    preq = gethtml(purl, hea)
    pjson = preq.json()
    pitem = pjson['data']
    if pitem is None:
        continue

    try:
        sql = 'delete from fa_wanlshop_goods_spu where goods_id=%s'
        id = (row[1],)

        mycursor.execute(sql, id)
        # mydb.commit()
        sql = 'delete from fa_wanlshop_goods_sku where goods_id=%s'
        id1 = (row[1],)

        mycursor.execute(sql, id1)
        # mydb.commit()
        spu = pitem['tier_variations']
        models = pitem['models']
        for k in range(len(spu)):
            spuname = spu[k]['name']
            item = ",".join(spu[k]['options'])
            sql = "INSERT INTO fa_wanlshop_goods_spu (name, item,goods_id) VALUES (%s, %s, %s)"
            val = (spuname, item, row[1])
            mycursor.execute(sql, val)
            spuid = mycursor.lastrowid

        for k in range(len(models)):
            # spuname=spu[k]['name']
            difference = models[k]['name']
            price = models[k]['price']
            if (len(str(price)) == 0):
                continue
            market_price = models[k]['price']
            stock = models[k]['stock']
            price = price * 0.00001 * 0.73
            market_price = market_price * 0.00001 * 0.73
            # market_price = str(market_price)[:-5]
            sn = 11
            sql = "INSERT INTO fa_wanlshop_goods_sku (difference, price,market_price,wholesale_price,stock,goods_id,weigh,sn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (difference, price, market_price, price, stock, row[1], 1, sn)
            mycursor.execute(sql, val)
            skuid = mycursor.lastrowid
            # mydb.commit()
        # a2 = html['items'][i]['item_basic']['name']

        # adr = ("Yellow Garden 2",)
        # ts = time.time()
        # sql = "update fa_wanlshop_goods set updatetime=%s where id=%s"
        # id = (ts, row[1])
        # mycursor.execute(sql, id)
        # spuid = mycursor.lastrowid
        # # mydb.commit()

    except Exception as e:
    # cursor.close()  # 先关游标
       mydb.rollback()
       print(e)
    finally:
        if (spuname.strip() == ''):
            mydb.rollback()
        if (difference.strip() == ''):
            mydb.rollback()
        mydb.commit()


