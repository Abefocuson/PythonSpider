
# coding=utf-8
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
 
    def createIssue(self):
        
        # issue_dict = { 
        # 'project': {'key': 'GLCR'},
        # 'issuetype': {'name': 'Bugs'},
        # 'summary': rule_title_en ,
        # 'customfield_11309':  {'value':  role_level},
        # 'customfield_11301': rule_title,      
        # 'customfield_11302':  {'value':  'C#'},
        # 'customfield_11305': role_noncompliant_code,
        # 'customfield_11306': role_compliant_code,
        # 'customfield_11310': role_id,
        # 'customfield_11304': role_desc,    
        # 'customfield_11303': role_desc_en                
        # }               
        #print issue_dict.encode('GBK')
        issue_dict = { 
        'project': {'key': 'GLCR'},
        'issuetype': {'name': 'Bugs'},
        'summary': 'This is a test of charset' ,
        'customfield_11309':  {'value':  '主要 Major '},
        'customfield_11301': '这是一个字符集测试',      
        'customfield_11302':  {'value':  'C#'},
        'customfield_11305': '这是一个字符集测试',
        'customfield_11306': '这是一个字符集测试',
        'customfield_11310': 'S0001',
        'customfield_11304': '这是一个字符集测试',    
        'customfield_11303': '这是一个字符集测试'                
        }  
        if self.jiraClinet == None:
            self.login()
        print issue_dict
        return self.jiraClinet.create_issue(issue_dict)

jiraTool = JiraTool()
jiraTool.login()

try:    
    result = jiraTool.createIssue()
    print '|'+ str(result)
  
    #f.write(json.dumps(role.__dict__,ensure_ascii=False).replace('&ensp;','')+',')
                
except Exception, e:
    print e;
    #excetionFile.write(str(e).encode('GBK'))
    