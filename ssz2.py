# 国外亚马逊商品爬虫
# 20200213
# https://www.amazon.com/dp/B07S3659V2


# -*- coding=utf-8 -*-
import fake_useragent
import requests
from fake_useragent import UserAgent
import re, os, time, random
from lxml import etree


def ua():
    location = os.getcwd() + '/fake_useragent.json'
    ua = fake_useragent.UserAgent(path=location)

    sjs = random.randint(1111111, 9999999)
    # print(sjs)
    sj = str(sjs)
    headers = {
        'User-Agent': ua.random,
        'Cookie': f'x-wl-uid=1eZRN4GNrthjZSGdfdsfds2WvlxT/sXztd0uB1drNz9lanSFUVhjkptreyjhXmvZLrY67w=; session-id=459-1321777-{sj}; ubid-acbcn=459-5647010-{sj}; lc-acbcn=zh_CN; i18n-prefs=CNY; session-token=g6hxLDDoHhzZLHWxd7FnNbtphW7mgdgdgda73azlryeyiS6M+c/4mKa3c/d/Pzgiv6gdgdgJx858blgOf+pmyxOtu55z5AlVE2nRoPAyWFMeG4OKmZQI3Lg5/MNhcN71PW9x2OkQWWLgdgdmxqaEQL9qGyYcnTbrYggdlInP0pROsR8oz; session-id-time=2082787201l; csm-hit=tb:s-KV6TYQQV77AQ5HHBPD94|1581595664859&t:1581595666568&adb:adblk_yes'
    }
    return headers


# 保存txt
def tx(id, text, path):
    print(f"正在保存商品数据..")
    with open(f'{path}{id}.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print(f">>>保存商品数据成功！")


# 下载图片
def down(img_url, img_name, path):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    print(f"下载{img_name}图片..")
    r = requests.get(img_url, headers=headers, timeout=10)
    with open(f'{path}{img_name}', 'wb') as f:
        f.write(r.content)
        print(f">>>下载{img_name}图片完成！")
    time.sleep(1)


def get_shopping(id):
    # id="B07S3659V2"
    # url="https://www.amazon.com/dp/B07S3659V2"
    url = f"https://www.amazon.com/dp/{id}"
    #url = f"https://www.aliexpress.com/item/4000542297628.html?spm=a2g0o.ams_97944.topranking.5.5238f4F2f4F2yX&pdp_ext_f=%7B%22ship_from%22:%22CN%22,%22sku_id%22:%2212000020015825027%22%7D&scm=1007.26694.226824.0&scm_id=1007.26694.226824.0&scm-url=1007.26694.226824.0&pvid=b2330d19-2700-478f-be59-8d73bf4e0abc&fromRankId=16043&_t=fromRankId:16043"
    html = requests.get(url, headers=ua(), timeout=20).content.decode('utf-8')
    # print(html)
    time.sleep(2)
    req = etree.HTML(html)
    title = re.findall(r'<title>Amazon.com: (.+?)</title>', html, re.S)[
        0]  # B&O PLAY by Bang & Olufsen Beoplay P6 便携式扬声器1140026 黑色
    print(title)
    path = f'{id}/'
    os.makedirs(path, exist_ok=True)  # 创建目录
    price = re.findall(r'"isPreorder":.+?,"price":(.+?),"doesMAPPolicyApply":.+?', html, re.S)[0]
    price = f'${price}'
    '''
    try:
        price=req.xpath('//span[@id="priceblock_saleprice"]/text()')[0]
    except:
        price = req.xpath('//span[@id="priceblock_ourprice"]/text()')[0]
    '''
    print(price)
    productdescriptions = req.xpath('//div[@id="productDescription"]//text()')
    productdescription = '\n'.join(productdescriptions)
    text = '%s%s%s%s%s%s%s' % (url, '\n', title, '\n', price, '\n', productdescription)
    tx(id, text, path)
    imgs = req.xpath('//span[@class="a-button-text"]/img/@src')
    for img in imgs:
        if 'jpg' in img:
            imgurl = img.split('._')[0]
            img_url = f'{imgurl}.jpg'
            img_name = img_url.split('/')[-1]
            print(img_url, img_name)
            down(img_url, img_name, path)

    print(f">>>下载图片完毕！")


if __name__ == '__main__':
    # id="B07XR5TRSZ"
    id = input("请输入要采集的商品id（比如：B07GJ2MWTZ）：")
    get_shopping(id)

