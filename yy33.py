import os,shutil
import re
import time
import datetime
import chardet
allFileNum = 0
myfile=[]
mydir=[]

def get_encode(file_my):
    file_my = open(file_my,mode='rb')  # 以二进制模式读取文件
    data = file_my.read()  # 获取文件内容
    file_my.close()  # 关闭文件
    result = chardet.detect(data)  # 检测文件内容
    return result["encoding"]
def printPath(level, path):
    global allFileNum
    ''''' 打印一个目录下的所有文件夹和文件 '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if (os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if (f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
                mydir.append(path + '/' + f)
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(f)
            myfile.append(path + '/' + f)
    # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        if (i_dl == 0):
            i_dl = i_dl + 1
        else:
            # print("得到的文件夹",'-' * (int(dirList[0])), dl)
            # 打印目录下的所有文件夹和文件，目录级别+1
            printPath((int(dirList[0]) + 1), path + '/' + dl)
    for fl in fileList:
        # print("得到的文件路径",'-' * (int(dirList[0])), fl)
        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1
def update_file(file_my):
    print("开始处理文件",file_my)
    #修改文件内容
    check_word=["111","222","333","4444","55","66"]
    change_word=["Learn_Java","learn01","learn02","learn03","learn04","learn05"]
    delete_word=["class"]
    old_name = file_my.split("/")[-1]
    if old_name.split(".")[1] in delete_word:
        os.remove(file_my)
    else:
        f = open(file_my, 'r')
        alllines = f.readlines()
        f.close()
        type_encode=get_encode(file_my)
        f = open(file_my, 'w+',encoding=type_encode)
        for eachline in alllines:
            for i in range(0,len(check_word)):
                eachline =eachline.replace(check_word[i],change_word[i])
            f.writelines(eachline)
        f.close()
        #修改文件名字
        base_path = file_my[:-len(old_name)]
        temp_old_name=old_name
        for i in range(0, len(check_word)):
            old_name = old_name.replace(check_word[i], change_word[i])
        os.rename(os.path.join(base_path,temp_old_name), os.path.join(base_path,old_name))
def update_folder(folder_my):
    print("开始处理文件夹",folder_my)
    #有一个规律，只有最后一个不同路径才是正确的，可修改的，否则就是之前修改过的，因此应该是逆序倒着修改
    charc_list=[]
    temp_folder=folder_my
    judge_name=folder_my.split("/")[-1]
    base_path=folder_my[:-len(judge_name)]
    temp_name=judge_name
    check_word = ["11","22"]
    change_word = ["Learn_Java","Learn_Java01"]
    for i in range(0, len(check_word)):
        judge_name = judge_name.replace(check_word[i], change_word[i])
    if temp_name!=judge_name:#如果名字变化说明不同了，应该修改
        os.rename(temp_folder,base_path+judge_name)
this_folder = input("\u9700\u8981\u66f4\u65b0\u4fe1\u606f\u7684\u4ee3\u7801\u8def\u5f84\uff1a").replace("\\",'/')
printPath(1, this_folder)
for i in myfile:
    print(i)
    i.replace("\\","/")
    update_file(i)
mydir=sorted(mydir,key=lambda x: len(x),reverse=True)
for i in mydir:
    print(i)
    update_folder(i)
input("已经处理完成，按任意键结束")