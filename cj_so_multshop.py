# -*- coding: utf-8 -*-
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
import requests
# from my_test import settings
import time
import pymysql
import threading

config= {
'host':'127.0.0.1',

'port':3306,

'user':'root',

'password':'tE9MKDewI5hfA5gT',

'db':'shop2',

'charset':'utf8mb4',

'cursorclass':pymysql.cursors.DictCursor,

}
STORE_PATH="D:/file/"

# 继承父类threading.Thread
class DownLoadPictures(threading.Thread):
    def __init__(self, name, sn):
        super().__init__()
        self.name = name
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',

                        'Referer': 'https://image.so.com/z?ch=beauty'}
        self.url = 'https://image.so.com/zjl?ch=beauty&sn={}'.format(sn)

        self.conn = pymysql.Connect(**config)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_resp_data(self):
        # print('当前是链接为{}的图片下载！'.format(self.url))
        print('当前是线程为{}的图片下载！'.format(self.name))
        # 返回的数据在json里
        sql="SELECT fa_wanlshop_goods.id,image,images FROM fa_wanlshop_goods WHERE fa_wanlshop_goods.shop_id ={}".format(self.name)
        self.cursor.execute(sql)

        row_list = self.cursor.fetchall()
        return row_list

    def run(self):
        # 重写run函数，线程在创建后会直接运行run函数
        resp_data = self.get_resp_data()
        dd=1
        # 判断是否还有图片
        if len(resp_data)>0:
            for elem in resp_data:
                image = elem['image']
                images = elem['images']
                # fromUrl = elem['purl']
                id = elem['id']
                self.download_picture(image, images, id)
        else:
            print('链接为{}已无图片'.format(self.url))

    def download_picture(self, image, images, id):
        image = image.split('/')[-1]
        sql = "select * from beautyImages where image = '{}'".format(image)
        row_count = self.cursor.execute(sql)
        if not row_count:
            try:
                # downloadurl="https://cf.shopee.sg/file/3ea865696f7ae06d87ff4e9c4c304c16?x-oss-process=image/auto-orient,1/interlace,1/format,jpg/quality,q_90/sharpen,50"
                images = images.split(',')
                for img in images:
                    resp = requests.get(img, verify=False)
                    img = img.split('/')[-1]
                    images1+=img+","
                    if resp.status_code == requests.codes.ok:
                        with open(STORE_PATH + '/' + img + '.jpg', 'wb') as f:
                            f.write(resp.content)
                            sql="update fa_wanlshop_goods set images1="



                resp = requests.get(image, verify=False)

                if resp.status_code == requests.codes.ok:
                    with open(STORE_PATH + '/' + image + '.jpg', 'wb') as f:
                         f.write(resp.content)

                print('下载完成')
                # 插入数据库
                insert_sql = "INSERT INTO beautyImages(image,  createTime) values (%s, %s)"
                try:
                    self.cursor.execute(insert_sql, (image,  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                    self.conn.commit()
                    print('插入标题为{}, 链接为{}成功!')
                except Exception:
                    print('插入标题为{}, 链接为{}失败, 失败原因是{}')
            except Exception:
                print('标题为{}， 链接为{}下载失败,失败原因是{}')
        else:
            print('标题为{}， 链接为{}已存在')


if __name__ == '__main__':
    start_time = time.time()
    thread_list = []
    conn = pymysql.Connect(**config)
    cursor=conn.cursor()
    cursor.execute("SELECT fa_wanlshop_goods.shop_id FROM fa_wanlshop_goods GROUP BY fa_wanlshop_goods.shop_id")
    fldata = cursor.fetchall()

    for i in range(0, len(fldata), 1):
        test = DownLoadPictures(name=str(fldata[i]["shop_id"]), sn=fldata[i]["shop_id"])
        thread_list.append(test)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    use_time = time.time() - start_time
    print('多线程用时：{}秒'.format(use_time))
