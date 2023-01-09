import json

import requests
from lxml import etree
import pandas as pd
import time
import re
import sys
import io
import MySQLdb
import mysql.connector

from lxml.html import tostring
from pandas import DataFrame
# sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")

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
            time.sleep(10)
            i += 1
    raise Exception()


def get_link(url, hea):
    req = gethtml(url, hea)
    html = etree.HTML(req.text)
    # type_link0 = html.xpath('//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/div/div/div[3]/div[2]/h2/a/span')  # 排除上级
    type_text = html.xpath('/html/body//a/span[@class="a-size-base-plus a-color-base a-text-normal"]')  # 排除上级
    end_img0 = html.xpath('//*[@class="sg-col-inner"]//div[@class="a-section aok-relative s-image-square-aspect"]//img[@class="s-image"]//@src')  # 排除上级
    end_link0 = html.xpath('//*[@class="sg-col-inner"]//a[@class="a-link-normal s-no-outline"]//@href')  # 排除上级

    # type_text = html.xpath('//*[@id="zg_browseRoot"]//span/text()')
    # end_link0 = html.xpath('//span[@class="zg_selected"]/../following-sibling::li[1]')  # 兄弟节点（之后）
    # end_link1 = html.xpath('//span[@class="zg_selected"]/../preceding-sibling::li[1]')  # 兄弟节点（之前）
    # if (len(end_link0) or len(end_link1)):
    #     end_link = 1
    # else:
    #     end_link = 0
    #     if (len(type_link0) == 1):
    #         print('***********',type_text)
    # time.sleep(5)
    return end_img0,type_text, end_link0







# url = 'https://www.amazon.com/-/en/%E9%94%80%E5%94%AE%E6%8E%92%E8%A1%8C%E6%A6%9C-Home-Kitchen-%E5%AE%B6%E5%85%B7/zgbs/home-garden/1063306/ref=zg_bs_unv_hg_2_17873917011_3'
url = 'https://www.amazon.com/s?k=perfume&language=en_US'

print(url)
hea = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'downlink': '8',
    'ect': '4g',
    'rtt': '250',
    'Cookie': "session-id=257-3500989-3695223; i18n-prefs=GBP; ubid-acbuk=257-5950834-2508848; x-wl-uid=1bEcLG2b03/1tAwPJNyfuRH+U7J9ZaPYejSBR4HXKuYQPJtLhQbDYyO/GOMypGKXqZrG7qBkS0ng=; session-token=x04EF8doE84tE+6CXYubsjmyob/3M6fdmsQuqzD0jwl/qGdO5aRc2eyhGiwoD0TFzK1rR/yziHsDS4v6cdqT2DySFXFZ9I5OHEtgufqBMEyrA0/Scr87KKA+GWOjfVmKRuPCqOGaixZQ6AIjU3e2iFOdM+3v90NeXFI3cazZcd6x9TYCy9b5u9V8zR7ePbdP; session-id-time=2082758401l; csm-hit=tb:MAA188S1G57TNTH6HQCZ+s-T9EGT4C8FC8J74X5T7CY|1594212767446&t:1594212767446&adb:adblk_no",
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}


type_link = []
type_text = []
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="tE9MKDewI5hfA5gT",
    database="spdata8"

)
mycursor = mydb.cursor()

type_link0,type_text0, end_link0 = get_link(url, hea)

for link1 in end_link0:
    url = link1
    if (url.find("s?k=")>-1):
        continue

    url = "https://www.amazon.com"+url+"&language=en"
    req = gethtml(url, hea)
    html = etree.HTML(req.text)
    title = html.xpath('//*[@id="productTitle"]/text()')
    title=title[0]
    price = html.xpath('//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]/span/span[@class="a-price-whole"]')
    price2 = html.xpath('//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]/span/span[@class="a-price-fraction"]')
    price21= html.xpath('//span[contains(@class, "priceToPay")]/span[2]/span[3]')
    desc= html.xpath('//*[@id="aplus_feature_div"]/div/div/div[1]')
    desc1= html.xpath("//h2[contains(.,'Product Description')]")
    desc2= html.xpath('//*[@id="aplus_feature_div"]')[0]
    original_html = tostring(desc2)
    # print(desc2[0].text)
    # .decode('utf-8')
    price = re.findall(r'var data = \{(.+?)\};', req.text, re.S)[0]
    bb = req.text.find("colorImages': { 'initial'")
    bb1 = req.text.find("colorToAsin': {'initial")
    tt = req.text[bb:bb1]


    pattern = re.compile(r'"displayPrice":"(.+?)"')  # 查找数字
    xsprice = pattern.findall(req.text)
    xsprice=xsprice[0]
    pattern = re.compile(r'"large":"(.+?)"')  # 查找数字
    result1 = pattern.findall(tt)
    a=2

    category_id = 0 #v2
    freight_id = 1
    shop_id = 1
    brand_id = 1
    grounding = 1
    specs = 'single'
    distribution = 'false'
    activity = 'false'
    views = 0
    description = ''
    stock = 9999
    sn = 11
    market_price=price
    item="color1"
    difference="color1"
    spuname="color"
    sql = 'Insert  Into `fa_wanlshop_wholesale1` (`title`,`image`,`images`,`price`,`wholesale_price`,`category_id`,`shop_id`,`brand_id`,`freight_id`,`grounding`,`specs`,`distribution`,`activity`,`views`,`content`,`proid`) Values (%s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    val = (
        title, "image", "images", xsprice, xsprice, category_id, -1, brand_id, freight_id, grounding, specs,
        distribution,
        activity, views, original_html, url)
    print(title)
    mycursor.execute(sql, val)
    goodsid = mycursor.lastrowid

    sql = "INSERT INTO fa_wanlshop_wholesale_spu1 (name, item,goods_id) VALUES (%s, %s, %s)"
    val = (spuname, item, goodsid)
    mycursor.execute(sql, val)
    spuid = mycursor.lastrowid

    sql = "INSERT INTO fa_wanlshop_wholesale_sku1 (difference, price,market_price,wholesale_price,stock,goods_id,weigh,sn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (difference, price, market_price, price, stock, goodsid, 1, sn)
    mycursor.execute(sql, val)
    skuid = mycursor.lastrowid

    # sql = 'Insert  Into `fa_wanlshop_wholesale` (`title`,`image`,`images`,`price`,`category_id`,`shop_id`,`brand_id`,`freight_id`,`grounding`,`specs`,`distribution`,`activity`,`views`,`content`,`proid`) Values (`%s`, `%s`, `%s`, %s, %s, %s,%s, %s, %s, `%s`, %s, %s, %s, `%s`, `%s`)' % (
    #     title, image, images, price, category_id, shop_id, brand_id, freight_id, grounding, specs,
    #     distribution,
    #     activity, views, description, proid)
    try:
        mycursor.execute(sql, val)
    except MySQLdb.Error as e:
        print(e)
    goodsid = mycursor.lastrowid
    # price = re.findall('', req.text, re.S)
    # price=price.strip()
    # price = "{"+price+"}"
    # price=price.rstrip()
    # # json_encode = json.dumps(price)
    # price = price.replace('"', '@@')
    # price = price.replace("'", '"')
    # price = price.replace("$", 'ttt')
    # price = price.replace("@@", "'")
    # b = eval(price)
    #
    # json_decode = json.loads(price)
    # //,strict=False

    # type_text = html.xpath('/html/body//a/span[@class="a-size-base-plus a-color-base a-text-normal"]')  # 排除上级

    url = "https://www.amazon.com/"+url


