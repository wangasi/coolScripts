# -*- coding: utf-8 -*-  
#---------------------------------------  
#   程序：thinkjs.org爬虫  
#   语言：Python 2.7   
#   作者：jiao.shen
#   github: http://github.com/wangasi
#   功能：将thinkjs使用文档html页面存储到本地。  
#   操作：先获得各级网页的路径，然后下载网页内容，过滤后存储到本地
#---------------------------------------  

import urllib
import urllib2
import thread 
import re
import os

think_base_url = 'https://thinkjs.org'

class Thinkjs_Spydier:

    def __init__(self):
        self.pathNames = []
        self.pages = []
        self.page = 1
        
    def QueryNetwork(self, lastUrl):
        myUrl = think_base_url + lastUrl 
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
        headers = { 'User-Agent' : user_agent }   
        req = urllib2.Request(myUrl, headers = headers)   
        try: response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print e.reason  
        myPage = response.read()
        return myPage
    
    def LoadPages(self, url, name, dirname):
        print name+"开始下载...\n"
        data = self.QueryNetwork(url)
        path = '/Users/iCrack/Desktop/thinkJS/'+ dirname
        #创建目录
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)

        f = open(path+'/'+name+'.html', 'w+')
        f.writelines(data)
        f.close()
        print name+"下载完成\n"

    def GetPathNames(self):
        home_content = self.QueryNetwork('/zh-cn/doc/2.2/index.html')

        #找到目标模块
        pattern = re.compile('<div.*?class="lbox doc-sidebar".*?>(.*?)</div>')
        detail_content = pattern.search(home_content).group(1)
        categoryItems = re.findall('<dl>(.*?)</dl>', detail_content, re.S)

        for item in categoryItems:
            nameMatch = re.search(r'<dt>(.*?)<dd>', item, re.S)
            title = u"无标题"
            if nameMatch:
                title = nameMatch.group(1)
            print title
            pathItems = re.findall('<a (.*?)/a>', item, re.S)
            childPaths = []
            for pathContent in pathItems:
                #key = pathContent.replace('href=.*?">',"")
                key = re.search('href=.*?>(.*?)<', pathContent,re.S).group(1)
                print key
                path = re.search('href="(.*?)">', pathContent,re.S).group(1)
                eDict = {"name": key, "path": path}
                childPaths.append(eDict)
                #下载网页
                thread.start_new_thread(self.LoadPages,(path, key, title))
                #self.LoadPages(path, key)
            mDict = {"title":title, "data": childPaths}
            self.pathNames.append(mDict)


    def StartScrapy(self): 
        self.GetPathNames()

#----------- 程序的入口处 -----------
print u'程序开始执行...'     
thinkSpyder = Thinkjs_Spydier()
thinkSpyder.StartScrapy()