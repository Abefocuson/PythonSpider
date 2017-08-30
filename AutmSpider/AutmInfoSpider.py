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
           
class AutmInfo:
      info_id=""
      info_website=""
      info_project_title=""    
      info_project_title_en=""    
      info_track_code=""
      info_origin_website=""
      info_short_description=""
      info_short_description_en=""
      info_abstract=""
      info_abstract_en="" 
      info_tags="" 
      info_posted_date=""
      info_primary="" 
      def __init__(self,info_id,info_website,info_project_title,info_project_title_en,info_track_code,info_origin_website,info_short_description,info_short_description_en,info_abstract,info_abstract_en,info_tags,info_posted_date,info_primary):
            self.info_id = info_id
            self.info_website = info_website
            self.info_project_title = info_project_title
            self.info_project_title_en = info_project_title_en
            self.info_track_code = info_track_code
            self.info_origin_website = info_origin_website
            self.info_short_description = info_short_description
            self.info_short_description_en = info_short_description_en
            self.info_abstract = info_abstract
            self.info_abstract_en = info_abstract_en
            self.info_tags = info_tags
            self.info_posted_date = info_posted_date
            self.info_primary = info_primary


dr = re.compile(r'<[^>]+>',re.S)
try:
    i=0;
    f = open('E:\AUTM\AutmSpider\\'+'json'+'.txt','a')
    excetionFile = open('E:\AUTM\AutmSpider\\'+'exception'+'.txt','a')
    try:
        for i in range(1,10):           
            
            url =  'https://gtp.autm.net/public/project/'  + str(i)
            print url
        
            autmInfo = AutmInfo('','','','','','','','','','','','','')
            try:
                html_1 = urllib2.urlopen(url).read()
            except Exception, e:
                print "----loop excetion----"+str(i)+"|"+str(e).encode('GBK');   
                excetionFile.write(str(e).encode('GBK'))
                continue
            if((str(html_1).find('You are trying to access an invalid Project'))<0):
                #i = i+1
                #print html_1
                SoupFather = BeautifulSoup(html_1,'lxml')
                #print SoupFather
                # print "----------- welcome-to-flintbox --------------"
                autmInfo.info_id = str(i)
                autmInfo.info_website = url
                autmInfo.info_project_title_en  = SoupFather.find_all(class_="welcome-to-flintbox")[0].text 
                autmInfo.info_project_title = googleTranslate(SoupFather.find_all(class_="welcome-to-flintbox")[0].text)
                # print "----------- key-value 0 --------------"
                # print SoupFather.find_all(class_="key-value")[0]
                # print "----------- key-value 1 --------------"

                for tr in SoupFather.find_all(class_="key-value")[1].find_all('tr'):
                
                    if (tr.find('th')):
                        trtext = tr.find('th').getText()
                        th = tr.find('th')
                        td = tr.find('td')
                        if(trtext =='Project Title'):
                            print "-----Project Title----"
                            # print th.getText() 
                            # print td.getText() 
                        if(trtext =='Track Code'):
                            print "-----Track Code----"
                            print th.getText()
                            autmInfo.info_track_code = td.getText() 
                        if(trtext =='Website'):
                            print "-----Website----"
                            print th.getText()
                            autmInfo.info_origin_website = td.getText() 
                        if(trtext =='Short Description'):
                            print "-----Short Description----"      
                            print th.getText().replace(u'\xa0', u' ')
                            autmInfo.info_short_description_en = td.getText().replace(u'\xa0', u' ')
                            autmInfo.info_short_description = googleTranslate(td.getText().replace(u'\xa0', u' '))
                        if(trtext =='Abstract'):
                            print "-----Abstract----"
                            print th.getText()
                            autmInfo.info_abstract_en = td.getText()
                            autmInfo.info_abstract = googleTranslate(td.getText())  
                        if(trtext =='Tags'):
                            print "-----Tags----"
                            print th.getText()
                            autmInfo.info_tags = td.getText() 
                        if(trtext =='Posted Date'):
                            print "-----Posted Date----"
                            print th.getText()
                            autmInfo.info_posted_date = td.getText() 
                print "----------- toolbox --------------"            
                for a in SoupFather.find_all(class_="toolbox")[0].find_all('a'):
                    if(a['href'].startswith('http://gtp.autm.net/public/group/')):
                        autmInfo.info_primary = a.string
                    if(a['href'].startswith('https://gtp.autm.net/public/group/')):
                        autmInfo.info_primary = a.string
                f.write(json.dumps(autmInfo.__dict__,ensure_ascii=False).replace('&ensp;','')+',')
            else:
                excetionFile.write("-----no content-----"+str(i).encode('GBK'))
    except Exception, e:
        print "----loop excetion----"+str(i)+"|"+str(e).encode('GBK');   
        excetionFile.write(str(e).encode('GBK'))        

except Exception, e:
    print str(e).encode('GBK');   
    excetionFile.write(str(e).encode('GBK'))

