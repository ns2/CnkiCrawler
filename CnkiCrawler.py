#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2,cookielib
import urllib
from bs4 import BeautifulSoup
import re
import sys
import time
import cStringIO
from PIL import Image
import cracker
import logging
type = sys.getfilesystemencoding()
reload(sys) 
sys.setdefaultencoding('utf-8') 


#import lxml.html.soupparser as soupparser 
#from lxml import etree

class Crawler:
    def __init__(self,nameList):
        self.nameList=nameList
        self.header={}
        self.url=''
        
    def __delete__(self):
        pass
    
    def setCrawlerParams(self):
        pass
    
    def outputData(self,data):
        print data
        
    def startCrawl(self):
        pass
      
      
class CnkiCrawler(Crawler):

    def __init__(self,nameList,ExtraOutInfo=True):
        logging.basicConfig(filename='./python_log.txt')
        self.logger=logging.getLogger("CnkiCrawler")
        self.logger.setLevel(logging.ERROR)
        self.nameList=nameList
        self.url='http://epub.cnki.net/'
        self.cookies=cookielib.CookieJar()
        self.outputHandler=printHref2Screen
        self.ExtraOutInfo=ExtraOutInfo
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(opener)
        
    def getUrlForFuzzy(self,name,type):
        url=self.url+'KNS/request/SearchHandler.ashx?action=&NaviCode=*&ua=1.11&PageName=ASP.brief_default_result_aspx&DbPrefix=SCOD&DbCatalog=%E4%B8%AD%E5%9B%BD%E5%AD%A6%E6%9C%AF%E6%96%87%E7%8C%AE%E7%BD%91%E7%BB%9C%E5%87%BA%E7%89%88%E6%80%BB%E5%BA%93&ConfigFile=SCDBINDEX.xml&db_opt=SCOD'
        url=url+'&txt_1_sel='+type
        url=url+'&txt_1_value1='+name
        url=url+'&txt_1_special1=%25&txt_1_extension=xls&his=0&parentdb=SCDB'
        return url
    
    def getUrlForExact(self,name,type):
        url=self.url+'/KNS/request/SearchHandler.ashx?action=&NaviCode=*&ua=1.21&PageName=ASP.brief_result_aspx&DbPrefix=SCOD&DbCatalog=%e4%b8%93%e5%88%a9%e6%95%b0%e6%8d%ae%e6%80%bb%e5%ba%93&ConfigFile=SCOD.xml&db_opt=%E4%B8%AD%E5%9B%BD%E4%B8%93%E5%88%A9%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E5%9B%BD%E5%A4%96%E4%B8%93%E5%88%A9%E6%95%B0%E6%8D%AE%E5%BA%93&db_value=%E4%B8%AD%E5%9B%BD%E4%B8%93%E5%88%A9%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E5%9B%BD%E5%A4%96%E4%B8%93%E5%88%A9%E6%95%B0%E6%8D%AE%E5%BA%93'
        url=url+'&txt_1_sel='+type
        url=url+'&txt_1_value1='+name
        url=url+'&txt_1_relation=%23CNKI_AND&txt_1_special1=%25&his=0&__=Fri%20May%2017%202013%2016%3A07%3A31%20GMT%2B0800%20(CST)'
        return url
        
    def crawl(self,name,type='SQR$=|',mode=0):
  
        logging.shutdown()
        if mode==0:
            url=self.getUrlForFuzzy(name,type)
        if mode==1:
            url=self.getUrlForExact(name,type)

        for i in range(3):
            try:
                urlInfo=urllib2.urlopen(url)
                break
            except:
                if self.ExtraOutInfo:
                    print 'Error when parsing the request url with',name
        aspSucc=urlInfo.read()
        aspUrl='http://epub.cnki.net/kns/brief/brief.aspx?pagename='+aspSucc
        
        for i in range(3):
            try:
                aspInfo=urllib2.urlopen(aspUrl)
                break
            except:
                if self.ExtraOutInfo:
                    print 'Error when parsing the asp url',name
        aspContent=aspInfo.read()
        """
        In order to get the content of cnki, we must at first post a url containing
        several parameters like name and type and some stuff, and then we can get 
        an asp url of the detailed contents, stored in aspContent
        """

        soup=BeautifulSoup(aspContent)
        hrefs=soup.find_all('span','countPageMark')
        if len(hrefs)==0:
            pageCounts=1
        else:
            pageCounts=int(hrefs[0].string[2:])
#        print hrefCounts

        crawledCount,pageNum=0,1
        currentSoup,currentPage=soup,aspContent
        numPerPage=20
        queryID=int(re.findall(r'queryid=\d*',currentPage)[0][8:])
        
        while pageNum<=pageCounts:
            
            if len(currentSoup.find_all('a','fz14'))==0:
                if self.ExtraOutInfo:
                    print 'validation code detected'
                self.cookies.clear()
       #         print("===========validate code page==========")
                
                for i in range(3):
                    try:
                        urlInfo=urllib2.urlopen(url)
                        break
                    except:
                        if self.ExtraOutInfo:
                            print 'Error when parsing the request url with',name
                aspSucc=urlInfo.read()
                aspUrl='http://epub.cnki.net/kns/brief/brief.aspx?pagename='+aspSucc
                for i in range(3):
                    try:
                        aspInfo=urllib2.urlopen(aspUrl)
                        break
                    except:
                        if self.ExtraOutInfo:
                            print 'Error when parsing the asp url',name
                aspContent=aspInfo.read()
#                print aspContent
                queryID=int(re.findall(r'queryid=\d*',aspContent)[0][8:])
#                pageNum=pageNum-1
                
            newPage='http://epub.cnki.net/kns/brief/brief.aspx?'
            newPage=newPage+'curpage='+str(pageNum)+'&RecordsPerPage='+str(numPerPage)+'&QueryID='+str(queryID)+'&ID=&turnpage=1&tpagemode=L&dbPrefix=SCOD&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx'
            for i in range(3):
                try:
                    currentPage=urllib2.urlopen(newPage)
                    break
                except:
                    if self.ExtraOutInfo:
                        print 'error when turn page from '+str(pageNum-1) + 'to' + str(pageNum)
            currentSoup=BeautifulSoup(currentPage)
            if len(currentSoup.find_all('a','fz14'))==0:
                if pageNum==1:
                    pageNum=pageNum+1
                continue
            for page in currentSoup.find_all('a','fz14'):
                contentUrl='http://dbpub.cnki.net/grid2008/dbpub'+page.get('href')[11:]
                contentPage=urllib2.urlopen(contentUrl).read()
                soup=BeautifulSoup(contentPage)
             #   print soup.contents
                if len(re.findall(u'您的IP',soup.find('p').text))!=0:
                    self.writeLog("IP Denied")
                    return
                while len(soup.findAll("input", {"id": "validateCode"}))!=0:
                    imgsrc=soup.find('img')['src'].encode('utf-8')
                    imageUrl='http://dbpub.cnki.net/grid2008/dbpub/'+imgsrc
                    imageFile= cStringIO.StringIO(urllib.urlopen(imageUrl).read())
                    img = Image.open(imageFile)
                    symbols=''.join(cracker.crack(img, './codelib'))
                    submitUrl='http://dbpub.cnki.net/grid2008/dbpub/'+soup.find('form')['action'].encode('utf-8')
                    submitRequest= urllib2.Request(submitUrl, data=urllib.urlencode({'validateCode':symbols,'submit':u'提交'}))
                    submitResponse = urllib2.urlopen(submitRequest)
                    contentPage = submitResponse.read()
                    soup=BeautifulSoup(contentPage)
                    if len(soup.findAll("input", {"id": "validateCode"}))!=0:
                        self.writeLog("Validate Fail")
                    else:
                        self.writeLog("Validate Success")
                    
                self.outputPage(contentPage)
                crawledCount=crawledCount+1
                time.sleep(0.1)
            if self.ExtraOutInfo:
                print 'parsing ' + name + ' with '+ str(pageNum) + ' pages finished, ' + str(pageCounts-pageNum) + ' pages left'
            pageNum=pageNum+1
        if self.ExtraOutInfo:
            print name + ' parse completed'
#        pageMarkRe=re.compile(r"<span class='countPageMark'>.*</span>")
#        print pageMarkRe.search(aspContent)

    def outputPage(self,page):
        self.outputHandler(page)
#        pass

    def setOutputHandler(self,outputHandler):
        self.outputHandler=outputHandler

    def crawlList(self,nameList):
        for name in nameList:
            self.crawl(name)
            
    def writeLog(self,msg):
        dateTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.logger.error(dateTime+" "+msg)

def printHref2Screen(page):
    print BeautifulSoup(page).title
    
def printSplitData2Screen(page):
    data=[]
    soup=BeautifulSoup(page)
    """
    ([Apply_ID]
           ,[Pub_ID]
           ,[Apply_Unit]
           ,[Inventors]
           ,[Agent_Firm]
           ,[Agent_Stuff]
           ,[CP_Code]
           ,[Abstract]
           ,[Prime_Item]
           ,[Pages]
           ,[Maj_Cmd]
           ,[Pat_Cmd]
           ,[Apply_Date]
           ,[Pub_Date]
           ,[PCT_Apply]
           ,[PCT_Pub]
           ,[Entry_Date])
    """
    if len(re.findall(u'国外',soup.title.text))!=0:
        checkItems=soup.findAll('td',{'class':'checkItem'})
        data.append(soup.head.title.text) #name
        data.append(checkItems[0].text) #Apply_ID
        data.append(checkItems[1].text) #Pub_ID
        data.append(checkItems[2].text) #Apply_Unit
        data.append(nextTd(checkItems[2]).text) #Inventors
        data.append('') #Agent_Firm
        data.append('') #Agent_Stuff
        data.append('') #CP_Code
        data.append(checkItems[6].text) #Abstract
        data.append('') #Prime_Item
        data.append('') #Pages
        data.append('') #Maj_Cmd
        data.append('') #Pat_Cmd
        data.append(''.join(nextTd(checkItems[0]).text.split('-'))) #Apply_Date
        data.append(''.join(nextTd(checkItems[1]).text.split('-'))) #Pub_Date
        data.append('') #PCT_Apply
        data.append('') #PCT_Pub
        data.append('') #Entry_Date
    else:
        checkItems=soup.findAll('td',{'class':'checkItem'})
        data.append(soup.head.title.text)
        data.append(checkItems[0].text) #Apply_ID
        data.append(checkItems[1].text) #Pub_ID
        data.append(stringWithoutEnter(checkItems[2].text)) #Apply_Unit
        data.append(stringWithoutEnter(checkItems[4].text)) #Inventors
        data.append(stringWithoutEnter(checkItems[7].text)) #Agent_Firm
        data.append(nextTd(checkItems[7]).text) #Agent_Stuff
        data.append(checkItems[9].text) #CP_Code
        data.append(stringWithoutEnter(checkItems[10].text)) #Abstract
        data.append(stringWithoutEnter(checkItems[11].text)) #Prime_Item
        data.append(checkItems[12].text) #Pages
        data.append(checkItems[13].text) #Maj_Cmd
        data.append(checkItems[14].text) #Pat_Cmd
        data.append(''.join(nextTd(checkItems[0]).text.split('-'))) #Apply_Date
        data.append(''.join(nextTd(checkItems[1]).text.split('-'))) #Pub_Date
        data.append(stringWithoutEnter(checkItems[5].text)) #PCT_Apply
        data.append(stringWithoutEnter(nextTd(checkItems[5]).text)) #PCT_Pub
        data.append(''.join(checkItems[6].text.split('-'))) #Entry_Date
        data.append(stringWithoutEnter(nextTd(checkItems[2]).text)) #Address
    formatData=''
    for dataItem in data:
        formatData=formatData+'\x1B'+dataItem
    print formatData[1:].encode('utf-8').decode('utf-8').encode(type)

def nextTd(tag):
    return tag.findNext('td').findNext('td')

def stringWithoutEnter(str):
    return ''.join(re.split('\s',str))


