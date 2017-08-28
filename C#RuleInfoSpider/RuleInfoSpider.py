#-*-coding:utf-8-*-
"""
Created on Wed Aug 03 11:36:12 2017

@author: Abe.wang
"""

from bs4 import BeautifulSoup
import re
import urllib2
import execjs  
import urllib
import chardet
import json
import sys
import goslate
import os
from jira import JIRA

reload(sys) 
sys.setdefaultencoding('utf-8')



class JiraTool:
    def __init__(self):
        self.server = 'http://10.10.192.9:8089'
        self.basic_auth = ('abe_code', '123456')
        self.jiraClinet = None
 
    def login(self):
        self.jiraClinet = JIRA(server=self.server, basic_auth=self.basic_auth)
        if self.jiraClinet != None:
            return True
        else:
            return False
 
    def findIssueById(self, issueId):
        if issueId:
            if self.jiraClinet == None:
                self.login()
                print self.jiraClinet.issue(issueId)
            return self.jiraClinet.issue(issueId)
        else:
            return 'Please input your issueId'
 
    def createIssue(self, rule_title_en, rule_title, role_level,role_noncompliant_code,role_compliant_code,role_id,role_desc,role_desc_en):
        
        issue_dict = { 
        'project': {'key': 'GLCR'},
        'issuetype': {'name': 'Bugs'},
        'summary': rule_title_en ,
        'customfield_11309':  {'value':  role_level},
        'customfield_11301': rule_title,      
        'customfield_11302':  {'value':  'C#'},
        'customfield_11305': role_noncompliant_code,
        'customfield_11306': role_compliant_code,
        'customfield_11310': role_id,
        'customfield_11304': role_desc,    
        'customfield_11303': role_desc_en                
        }
               
        #print issue_dict.encode('GBK')
        #print issue_dict
        if self.jiraClinet == None:
            self.login()
        print issue_dict
        return self.jiraClinet.create_issue(issue_dict)


def GetRoleLevel(roldId):
      print roldId
      try:
        html_1 = urllib2.urlopen('https://sonarcloud.io/api/rules/show?key=csharpsquid%3A'+roldId).read()
      except Exception as e: 
        #return "ERROR"
        return "次要 Minor"
      #print html_1      
      TypeSoup = BeautifulSoup(html_1,'lxml')
      #print TypeSoup
      if((str(TypeSoup).find('"severity":"BLOCKER"'))>0):
            return "阻断 Block"
      if(str(TypeSoup).find('"severity":"MAJOR"')>0):
            return "主要 Major "
      if(str(TypeSoup).find('"severity":"MINOR"')>0):
            return "次要 Minor"
      if(str(TypeSoup).find('"severity":"CRITICAL"')>0):
            return "严重 Critical"
   
       
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    #print pathDir
    filearrs = []
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题
        filearrs.append(child)
    return filearrs

def GetRole(roleClass):
    if((str(roleClass).find('filter_Bug_Detection'))>0):  
        return "Bug"
    if((str(roleClass).find('filter_Code_Smell_Detection'))>0):  
        return "CodeSmell"
    if((str(roleClass).find('filter_Vulnerability_Detection'))>0):  
        return "Vulnerability"

def YudaoTranslator(content):
      url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=http://www.youdao.com/'
     
      data = {}
      data['type'] = 'AUTO'
      data['i'] = content
      data['doctype'] = 'json'
      data['xmlVersion'] = '1.6'
      data['keyfrom'] = 'fanyi.web'
      data['ue'] = 'UTF-8'
      data['typoResult'] = 'true'
     
      data = urllib.urlencode(data)     
      response = urllib.urlopen(url, data)     
      html = response.read()     
      target = json.loads(html)      
      result = target["translateResult"][0][0]['tgt']
      return result

def GoslateTranslator(content):
      gs = goslate.Goslate()
      print content
      return  gs.translate(content, 'cn')


class Py4Js():  
    def __init__(self):  
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
 
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 
 
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 
 
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)  
  
    def getTk(self, text):  
        return self.ctx.call("TL", text)  
  
  
  
def open_url(url):  
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib2.Request(url=url, headers=headers)  
    response = urllib2.urlopen(req)  
    data = response.read().decode('utf-8')  
    return data  
  
  
def googleTranslateSingleSentence(content):  
    js = Py4Js()  
    tk = js.getTk(content)  
  
    content = urllib2.quote(content)  
    url = "http://translate.google.cn/translate_a/single?client=t" \
          "&tl=zh-CN&sl=EN&hl=EN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
          "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, content)  
  
    result = open_url(url)
    #print url

    end = result.find("\",")  
    if end > 4:  
        texts = result[4:end]
    return texts
  
  
def googleTranslate(content):
    temp = ''
    texts=content.split('.')  
    results=''
    tempTranslateResults = ''  
    for i in range(len(texts)):  
        try:
            tempTranslateResults = googleTranslateSingleSentence(str(texts[i])) 
            #print '['+str(i)+']'  + tempTranslateResults
            results = results + tempTranslateResults +'.'
        except Exception as e:  
            temp =  e  
    return results

def googleTranslateAll(content):
    temp = ''
    texts=content.strip()  
    results=''
    tempTranslateResults = ''  
    #print content
    try:
        tempTranslateResults = googleTranslateSingleSentence(str(texts)) 
        #print '['+str(texts)+']'  + tempTranslateResults
        results = results + tempTranslateResults
    except Exception as e:  
            temp =  e  
    return results


def removeSpecialChar(content):
    
    return str(content).replace('&gt;','>').replace('&lt;','<').replace('&amp;','&').replace('&quot;','"').replace('&ensp;','').replace('＆lt;','<').replace('＆gt;','>').replace('＆amp;','&').replace('＆quot;','"').replace('＆ensp;','')
    

def Obj_dict(obj):
    return obj.__dict__

class roleInfo:
      role_id=""
      role_origin_id=""
      role_type=""    
      role_title=""
      role_title_en=""
      role_desc=""
      role_desc_en=""
      role_noncompliant_code=""
      role_compliant_code="" 
      def __init__(self,role_id,role_origin_id,role_type,role_level,role_title,role_title_en,role_desc,role_desc_en,role_have_noncompliant_code,role_noncompliant_code,role_have_compliant_code,role_compliant_code):
            self.role_id = role_id
            self.role_origin_id = role_origin_id
            self.role_type = role_type
            self.role_level = role_level
            self.role_title = role_title
            self.role_title_en = role_title_en
            self.role_desc = role_desc
            self.role_desc_en = role_desc_en
            self.role_have_noncompliant_code = role_have_noncompliant_code
            self.role_noncompliant_code = role_noncompliant_code
            self.role_have_compliant_code = role_have_compliant_code
            self.role_compliant_code = role_compliant_code
           

dr = re.compile(r'<[^>]+>',re.S)


# html_1 = urllib2.urlopen('https://www.sonarsource.com/products/codeanalyzers/sonarcsharp/rules.html').read()
# SoupFather = BeautifulSoup(html_1,'lxml')

arrHtmlFileList = eachFile('special')
# jiraTool = JiraTool()
# jiraTool.login()
for file in arrHtmlFileList:

      SoupFather = BeautifulSoup(open(file),'lxml')

      SoupFather.find_all(class_="rule")
      print len(SoupFather.find_all(class_="rule-title"))
      print len(SoupFather.find_all(class_="rule"))
      print len(SoupFather.find_all(re.compile("rule_RSPEC-")))
      print len(SoupFather.find_all(class_="filter_Code_Smell_Detection"))
    #  i = 1

    #   for child in SoupFather.find_all(class_="rule"):
    #         role = roleInfo('','','','','','','','','','','','')
    #         #print len(SoupFather.find_all(class_="rule"))
    #         i += 1
    #         print i
    #         f = open('E:\AUTM\C#RuleInfoSpider\\'+file+'.txt','a')
    #         excetionFile = open('E:\AUTM\C#RuleInfoSpider\\'+'exception'+'.txt','a')
    #         Soup = BeautifulSoup(str(child),'lxml')
    #         #print Soup
    #         print Soup.li.attrs['id']#original id
    #         #print Soup.li.attrs['class']#original id           
    #         role.role_origin_id = Soup.li.attrs['id']
    #         role.role_id = 'S'+ Soup.li.attrs['id'].replace('rule_RSPEC-', '')
    #         role.role_level = GetRoleLevel(role.role_id)
    #         print role.role_level
    #         role.role_type = GetRole(Soup.li.attrs['class'])
    #         # print role.role_level
    #         # print role.role_type
    #         # print Soup.label.text.strip()
    #         role.role_title_en = removeSpecialChar(Soup.label.text.strip())
    #         # print googleTranslate(Soup.label.text.strip())      
    #         role.role_title = removeSpecialChar(googleTranslate(Soup.label.text.strip()))
    #         print role.role_title
    #         for child in Soup.find_all(class_="rule-description")[0].children:
    #               if (child.name == 'p'):
    #                     #print type(child)
    #                     #print dr.sub('',str(child)).replace('<class \'bs4.element.Tag\'>', '').replace('&ensp;','')
    #                     role.role_desc_en += removeSpecialChar(dr.sub('',str(child)).replace('<class \'bs4.element.Tag\'>', ''))
    #                     role.role_desc += removeSpecialChar(googleTranslate(dr.sub('',str(child)).replace('<class \'bs4.element.Tag\'>', '')))
    #               if (child.name == 'h2'):
    #                     break

    #         Noncomplianttag = False;
    #         Complianttag = False;

    #         for child in Soup.find_all(class_="rule-description")[0].children:
    #               if (child.name == 'h2'):
    #                     if (child.text == 'Noncompliant Code Example'):
    #                           Noncomplianttag = True
    #                     if (child.text == 'Compliant Solution'):
    #                           Complianttag = True
    #               if (child.name == 'div'):
    #                     if(Noncomplianttag):
    #                           #print "Noncompliant Code Example"
    #                           #print dr.sub('',str(child))
    #                           role.role_have_noncompliant_code = 'Y'
    #                           role.role_noncompliant_code = removeSpecialChar(dr.sub('',str(child)))
    #                           Noncomplianttag = False
    #                     if(Complianttag):
    #                           print "Compliant Solution"
    #                           print dr.sub('',str(child))
    #                           role.role_have_compliant_code = 'Y'
    #                           role.role_compliant_code = removeSpecialChar(dr.sub('',str(child)))
    #                           Complianttag = False


    #         print "---------------------------------------"
    #         print role.role_desc
    #         # desccode=chardet.detect(role.role_desc)
    #         # titlecode=chardet.detect(role.role_title)
    #         # levelcode=chardet.detect(role.role_level)
    #         # print desccode
    #         # print titlecode
    #         # print levelcode

    #         if (len(role.role_noncompliant_code)<=1):
    #             role.role_noncompliant_code = '无'
    #         if (len(role.role_desc)<=1):
    #             role.role_desc = '无'
    #         try:
    #             #result = 'OK'
    #             result = jiraTool.createIssue(role.role_title_en, role.role_title, role.role_level,role.role_noncompliant_code,role.role_compliant_code,role.role_id,role.role_desc,role.role_desc_en)
    #             print str(role.role_id) +'|'+ str(result)
    #             f.write(str(role.role_id) +'|'+ str(result)+'\n')
    #             #f.write(json.dumps(role.__dict__,ensure_ascii=False).replace('&ensp;','')+',')
                
    #         except Exception, e:
    #             print str(e).encode('GBK');
    #             f.write(str(role.role_id) +'|'+'\n')
    #             excetionFile.write(str(e).encode('GBK'))
    #             continue
            #f.write(json.dumps(role.__dict__,ensure_ascii=False).replace('&ensp;','')+',')
