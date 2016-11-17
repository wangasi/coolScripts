#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-11-02 15:37:41
# Project: novel

from pyspider.libs.base_handler import *
import urllib,http.client
import ujson
import re,os

CN_NUM = {
u'〇' : 0,
u'一' : 1,
u'二' : 2,
u'三' : 3,
u'四' : 4,
u'五' : 5,
u'六' : 6,
u'七' : 7,
u'八' : 8,
u'九' : 9,
 
u'零' : 0,
u'壹' : 1,
u'贰' : 2,
u'叁' : 3,
u'肆' : 4,
u'伍' : 5,
u'陆' : 6,
u'柒' : 7,
u'捌' : 8,
u'玖' : 9,
 
u'貮' : 2,
u'两' : 2,
}
CN_UNIT = {
u'十' : 10,
u'拾' : 10,
u'百' : 100,
u'佰' : 100,
u'千' : 1000,
u'仟' : 1000,
u'万' : 10000,
u'萬' : 10000,
u'亿' : 100000000,
u'億' : 100000000,
u'兆' : 1000000000000,
}

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.09xs.com/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.nav a').items():  
            self.crawl(each.attr.href, callback=self.index_page)
        for each in response.doc('td a').items():
            self.crawl(each.attr.href, callback=self.index_page)
        for each in response.doc('.l .s2 > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
            
    #获得小说信息   
    def detail_page(self, response):
        bookName = response.doc('h1').text()
        bookInfo = ""
        for each in response.doc('#info > p').items():
            bookInfo += each.text()
        desc = response.doc("#intro > p").text()
        
        bookInfo = bookInfo.split('：')
        author = bookInfo[1].split()[0]
        
        imageURL = response.doc('#sidebar img').attr.src
        category = response.doc('.con_top').text().split('>')
        keyword = category[1].strip()
        
        data = urllib.parse.urlencode({'novel_name':bookName,
                'novel_author': author,
                'novel_desc':desc,
                'novel_image':imageURL,
                'novel_regiment': keyword,
                'novel_keywords': keyword})
        headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}
        conn = http.client.HTTPConnection('localhost',8360,timeout=30)
        conn.request('POST', '/novel/writenovel/addnovel', data, headers) 
        req = conn.getresponse()
        reback = ujson.loads(req.read())
 
        if reback["errno"] == 0:
            bookId = reback["data"]
            for each in response.doc('dd > a').items():
                self.crawl(each.attr.href, callback=self.content_page,save={'book_id':bookId['book_id'],'keyword':keyword})
    
    #获得章节信息
    def content_page(self, response):
        bookId = response.save
        print (bookId)
        chapterName = response.doc('title').text().split('_')[0]
        chapterId = re.sub('\D',"",chapterName)
        ids = chapterName.split()[0]
        print (ids)
        if not chapterId or chapterId == 0:
            lcn = list(ids)
            unit = 0 #当前的单位
            ldig = []#临时数组
            while lcn:
                cndig = lcn.pop()
                if cndig in CN_UNIT:
                    unit = CN_UNIT.get(cndig)
                    if unit==10000:
                        ldig.append('w')    #标示万位
                        unit = 1
                    elif unit==100000000:
                        ldig.append('y')    #标示亿位
                        unit = 1
                    elif unit==1000000000000:#标示兆位
                        ldig.append('z')
                        unit = 1
                    continue
                else:
                    dig = CN_NUM.get(cndig)
                    if unit:
                        dig = dig*unit
                        unit = 0
                    ldig.append(dig)
            if unit==10:    #处理10-19的数字
                ldig.append(10)
            ret = 0
            tmp = 0
            length = 0
            numbers = []
            while ldig:
                x = ldig.pop()
                if x=='w':
                    tmp *= 10000
                    ret += tmp
                    tmp=0
                elif x=='y':
                    tmp *= 100000000
                    ret += tmp
                    tmp=0
                elif x=='z':
                    tmp *= 1000000000000
                    ret += tmp
                    tmp=0
                elif x:
                    length += 1
                    numbers.append(x)
                    tmp += x
            if tmp == 0 and numbers[0] < 10 and length > 1:
                tmp = 0
                for i in range(0, len(numbers)):
                    tmp += numbers[i]*10**(length-1-i)
               
            ret += tmp
            chapterId = ret
            print(chapterId)
        content = response.doc('#content').text()
        fileName = chapterName+'.html'
        dirname = '/novel_content/'+bookId['keyword']+'/'+ fileName
        path = '/Users/iCrack/Desktop/myWeb/novel_content/'+ bookId['keyword']
        #创建目录
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)

        f = open(path+'/'+fileName, 'w+')
        f.writelines(content)
        f.close()
        
        data = urllib.parse.urlencode({'chapter_novelid': bookId['book_id'],
                'chapter_chapterid': chapterId,
                'chapter_contentURL': dirname,
                'chapter_name':chapterName})
        headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}
        conn = http.client.HTTPConnection('localhost',8360,timeout=30)
        conn.request('POST', '/novel/writenovel/addchapter', data, headers) 
        req = conn.getresponse()
        reback = req.read()
        print(reback)