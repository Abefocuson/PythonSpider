from bs4 import BeautifulSoup
import re
import urllib2
import urllib
import chardet
import math
import json


url = "http://www.weixinqun.com/group?id=1" # person have one qrcode group has two


def IsThisUrlAvailible(url):
      try:
            resp = urllib2.urlopen(url)
            contents = True
      except urllib2.HTTPError, error:
            contents = False
      return contents

#def IsThisUrlHaveImage(url):
#html_1 = urllib2.urlopen(url).read()
#print IsThisUrlAvailible(url)

class groupInfo:
      url=""
      type=""    
      personQrCodeFilePath=""
      groupQrCodeFilePath=""
      publicQrCodeFile=""
      otherInfo=""
      def __init__(self,url,type,personQrCodeFilePath,groupQrCodeFilePath,publicQrCodeFile,otherInfo):
            self.url = url
            self.type = type
            self.personQrCodeFilePath = personQrCodeFilePath
            self.groupQrCodeFilePath =groupQrCodeFilePath
            self.publicQrCodeFile = publicQrCodeFile
            self.otherInfo = otherInfo

#oneTest = GroupInfo("1","1","1","1","1")
oneTest = groupInfo('1','1','1','1','1','1')

print JSON(oneTest)

#for imgsrc in link.find_all('img'):
   #   print(link.get('src'))
   #   print(link.get('alt'))

#print html_1
# encoding_dict = chardet.detect(html_1)
# #print encoding
# web_encoding = encoding_dict['encoding']
# print web_encoding

# if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
    
#   html = html_1.decode('utf-8').encode('GBK')
# else :
#    html = html_1.decode('gbk','ignore').encode('utf-8').encode('gbk')
# file_object = open('thefile.txt', 'w')
# file_object.write(html_1)
# file_object.close( )
#print html_1

