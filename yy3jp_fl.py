import re

import zhconv
import os
from googletrans import Translator
import mysql.connector
# googletrans==4.0.0-rc1
allFileNum = 0
kk = 0
def repl_func(matched):
    global kk

    if matched:
        kk += 1
        text = matched.group(0)
        return "$"+str(kk)+"$"+str(text)+"$"+str(kk)+"$"
def repl_func1(matched):
    global kk

    if matched:
        kk += 1
        text = matched.group(0)
        return "$"+str(kk)+"$"+str(text)+"$"+str(kk)+"$"



def transform2_zh_hant(string):
    new_str = zhconv.convert(string, 'zh-hant')
    return new_str


def transform2_zh_hans(string):
    new_str = zhconv.convert(string, 'zh-hans')
    return new_str


if __name__ == '__main__':
    string = "pen45导火www线hello"
    if __name__ == '__main__':
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="tE9MKDewI5hfA5gT",
            # database="shopry"
            database="spdata8"

        )
        mycursor = mydb.cursor()
        translator = Translator()
        mycursor.execute("select name,id from fa_wanlshop_category where type='goods' order by id asc")

        fldata = mycursor.fetchall()
        for row in fldata:
            # for index in range(len(result)):
            fyres = translator.translate(row[0], dest='id').text
            # dic.setdefault("$"+str(index+1)+"$"+str(result[index])+"$"+str(index+1)+"$",[]).append(fyres)
            # dic1[index] = fyres
            sql = "update  fa_wanlshop_category set idname='%s' where id=%s" % (fyres, row[1])
            mycursor.execute(sql)
            mydb.commit()
        # printPath(1, 'G:/ac8/lang')
        print ('总文件数 =', allFileNum)

        # with open("H:/ShadowsocksR/chat.vue",encoding = "utf-8") as f:
    #     a = f.read()
    # string2 = transform2_zh_hant(a)
    # with open("H:/ShadowsocksR/chat.vue", "w+") as fw:
    #     fw.write(string2)
    # print(string2)
    # string3 = transform2_zh_hans(string2)
    # print(string3)