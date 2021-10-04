import zhconv
import os
allFileNum = 0
def printPath(level, path):
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
        # 打印文件
        print ('-s2' * (int(dirList[0])), fl)
        with open(path+ '/' +fl,encoding = "utf-8",errors='ignore') as f:
            a = f.read()
        string2 = transform2_zh_hant(a)
        with open(path+ '/' +fl, "w+",encoding='utf-8',errors='ignore') as fw:
            fw.write(string2)
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
        printPath(1, 'H:/ShadowsocksR/tt')
        print ('总文件数 =', allFileNum)

        # with open("H:/ShadowsocksR/chat.vue",encoding = "utf-8") as f:
    #     a = f.read()
    # string2 = transform2_zh_hant(a)
    # with open("H:/ShadowsocksR/chat.vue", "w+") as fw:
    #     fw.write(string2)
    # print(string2)
    # string3 = transform2_zh_hans(string2)
    # print(string3)