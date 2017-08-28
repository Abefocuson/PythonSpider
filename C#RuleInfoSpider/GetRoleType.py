# -*- coding=utf-8 -*-  
"""
Created on Wed Aug 03 11:36:12 2017

@author: Abe.wang
"""

from bs4 import BeautifulSoup
import re
import urllib2
import urllib
import chardet
import json

def getRoleType(roldId):
    html_1 = urllib2.urlopen('https://sonarcloud.io/api/rules/show?key=csharpsquid%3A'+roldId).read()
    TypeSoup = BeautifulSoup(html_1,'lxml')
    if(str(TypeSoup).find('"severity":"BLOCKER"'))>0
        return "BLOCKER"
    if(str(TypeSoup).find('"severity":"MAJOR"'))>0
        return "MAJOR"
    if(str(TypeSoup).find('"severity":"MINOR"'))>0
        return "MINOR"
    if(str(TypeSoup).find('"severity":"CRITICAL"'))>0
        return "CRITICAL"

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
      def __init__(self,role_id,role_origin_id,role_type,role_title,role_title_en,role_desc,role_desc_en,role_have_noncompliant_code,role_noncompliant_code,role_have_compliant_code,role_compliant_code):
            self.role_id = role_id
            self.role_origin_id = role_origin_id
            self.role_type = role_type
            self.role_title = role_title
            self.role_title_en = role_title_en
            self.role_desc = role_desc
            self.role_desc_en = role_desc_en
            self.role_have_noncompliant_code = role_have_noncompliant_code
            self.role_noncompliant_code = role_noncompliant_code
            self.role_have_compliant_code = role_have_compliant_code
            self.role_compliant_code = role_compliant_code
           

dr = re.compile(r'<[^>]+>',re.S)

role = roleInfo('','','','','','','','','','','')

SoupFather = BeautifulSoup(open('allindex.html'),'lxml')

SoupFather.find_all(class_="rule")

for child in SoupFather.find_all(class_="rule"):      
    Soup = BeautifulSoup(str(child),'lxml')
      #print Soup
    print Soup.li.attrs['id']#original id
    role.role_origin_id = Soup.li.attrs['id']
    role.role_id = 'S'+ Soup.li.attrs['id'].replace('rule_RSPEC-', '')
    html_1 = urllib2.urlopen('https://sonarcloud.io/api/rules/show?key=csharpsquid%3AS2930').read()
    TypeSoup = BeautifulSoup(html_1,'lxml')
    print  (str(TypeSoup).find('"severity":"BLOCKER"'))