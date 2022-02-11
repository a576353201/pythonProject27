import requests
# from my_test import settings
import sys
import time
import pymysql



config= {
'host':'127.0.0.1',

'port':3306,

'user':'root',

'password':'tE9MKDewI5hfA5gT',

'db':'cjso',

'charset':'utf8mb4',

'cursorclass':pymysql.cursors.DictCursor,

}


class DownLoadPictures(object):
    def __init__(self, sn):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                        'Referer': 'https://image.so.com/z?ch=beauty'}
        self.url = 'https://image.so.com/zjl?ch=beauty&sn={}'.format(sn)

        self.conn = pymysql.Connect(**config)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_resp_data(self):
        print('当前是链接为{}的图片下载！'.format(self.url))
        # 返回的数据在json里
        resp = requests.get(self.url, headers=self.headers)
        return resp.json()

    def get_download_url(self):
        resp_data = self.get_resp_data()
        # 判断是否还有图片
        if resp_data['end'] is False:
            for elem in resp_data['list']:
                downloadurl = elem['qhimg_downurl']
                fromUrl = elem['purl']
                title = elem['title']
                self.download_picture(downloadurl, title, fromUrl)
        else:
            print('链接为{}已无图片'.format(self.url))

    def download_picture(self, downloadurl, title, fromUrl):
        sql = "select * from beautyImages where downloadUrl = '{}' and title='{}'".format(downloadurl, title)
        row_count = self.cursor.execute(sql)
        if not row_count:
            try:
                resp = requests.get(downloadurl, headers=self.headers)
                if resp.status_code == requests.codes.ok:
                    with open(settings.STORE_PATH + '/' + title + '.jpg', 'wb') as f:
                        f.write(resp.content)
                print('下载完成')
                # 插入数据库
                insert_sql = "INSERT INTO beautyImages(title, downloadUrl, fromUrl, createTime) values (%s, %s, %s, %s)"
                try:
                    self.cursor.execute(insert_sql, (title, downloadurl, fromUrl, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                    self.conn.commit()
                    print('插入标题为{}, 链接为{}成功!'.format(title, downloadurl))
                except Exception:
                    print('插入标题为{}, 链接为{}失败, 失败原因是{}'.format(title, downloadurl, sys.exc_info()[1]))
            except Exception:
                print('标题为{}， 链接为{}下载失败,失败原因是{}'.format(title, downloadurl, sys.exc_info()[1]))
        else:
            print('标题为{}， 链接为{}已存在'.format(title, downloadurl))


if __name__ == '__main__':
    start_time = time.time()
    for i in range(0, 301, 30):
        test = DownLoadPictures(sn=i)
        test.get_download_url()
    use_time = time.time() - start_time
    print('单线程用时：{}秒'.format(use_time))

