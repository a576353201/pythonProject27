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
def printPath(level, path):
    global kk
    global allFileNum
    ''''' 
    打印一个目录下的所有文件夹和文件 
    '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if(os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if(f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if(os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(f)
    # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        if(i_dl == 0):
            i_dl = i_dl + 1
        else:
            # 打印至控制台，不是第一个的目录
            print ('-s1' * (int(dirList[0])), dl)
            # 打印目录下的所有文件夹和文件，目录级别+1
            printPath((int(dirList[0]) + 1), path + '/' + dl)
    for fl in fileList:
        ext=os.path.splitext(fl)[-1]
        # if(fl!='tr.php'):
        #     continue
        if(ext!='.php'):
            continue
        # if(ext=='.js'):
        #     continue
        # 打印文件
        print ('-s2' * (int(dirList[0])), fl)
        with open(path+ '/' +fl,encoding = "utf-8",errors='ignore') as f:
            a = f.read()
            result = re.findall('[\u4e00-\u9fa5]+', a)
            if len(result)==0:
                continue


            thstr=re.sub('[\u4e00-\u9fa5]+', repl_func, a)
            kk=0
            translator = Translator()
            # translator = Translator(service_urls=[
            #     'translate.google.com',
            #     'translate.google.co.kr',
            # ])

        fy=translator.translate('我是中国人.', dest='tr').text

        dic = {}
        dic1 = {}
        fylist=[]
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="tE9MKDewI5hfA5gT",
            # database="shopry"
            database="shop2"

        )
        mycursor = mydb.cursor()
        mycursor.execute("select name,id from fa_wanlshop_category where type='goods' order by id asc")

        fldata = mycursor.fetchall()
        for row in fldata:
        # for index in range(len(result)):
            fyres = translator.translate(row[0], dest='id').text
            # dic.setdefault("$"+str(index+1)+"$"+str(result[index])+"$"+str(index+1)+"$",[]).append(fyres)
            # dic1[index] = fyres
            sql = 'update  fa_wanlshop_category set idname=%s where id=%s' % (fyres, row[1]);
            mycursor.execute(sql)

            # fy[index]['from']=result[index]
            # fy[index]['to']=fyres
            dd=2


        #

        # for di in dic.items():
        #     thstr=thstr.replace(di[0],di[1][0],1)



        # thstr1 = re.sub('[\u4e00-\u9fa5]+', repl_func, thstr)
        # string2 = transform2_zh_hant(a)


        # with open(path+ '/' +fl, "w+",encoding='utf-8',errors='ignore') as fw:
        #     d=2
        #     fw.write(thstr)
        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1


def transform2_zh_hant(string):
    new_str = zhconv.convert(string, 'zh-hant')
    return new_str


def transform2_zh_hans(string):
    new_str = zhconv.convert(string, 'zh-hans')
    return new_str


if __name__ == '__main__':
    string = "pen45导火www线hello"
    if __name__ == '__main__':
        printPath(1, 'G:/jz/www.t.com/application/api/lang/id')
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