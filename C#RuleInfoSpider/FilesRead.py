
#-*- coding: UTF-8 -*- 

'''
读取指定目录下的所有文件

'''
import os
# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    #print pathDir
    filearrs = []
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题
        filearrs.append(child)
    return filearrs


# print eachFile('E:\AUTM\C#RuleInfoSpider\html')
# print '----------------'
print eachFile('html')