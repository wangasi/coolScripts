# -*- coding: utf-8 -*-  
#---------------------------------------  
#   程序：百度贴吧爬虫  
#   版本：0.1  
#   语言：Python 2.7  
#   操作：输入带分页的地址，去掉最后面的数字，设置一下起始页数和终点页数。  
#   功能：下载对应页码内的所有页面并存储为html文件。  
#--------------------------------------- 

import string, urllib2

#定义百度函数
def baidu_tieba(url, begin_page, end_page):
	for i in range(begin_page,end_page+1):
		sName = string.zfill(i, 5) + '.html'
		print '正在下载第' + str(i) + '个网页，并将其存储为' + sName + '.......'
		f = open(sName, 'w+')
		m = urllib2.urlopen(url+str(i)).read()
		f.write(m)
		f.close()



#-------- 在这里输入参数 ------------------  
  
# 这个是山东大学的百度贴吧中某一个帖子的地址  
#bdurl = 'http://tieba.baidu.com/f?kw=%E5%85%94%E5%AD%90&ie=utf-8&'  
#iPostBegin = 2  
#iPostEnd = 10 

bdurl = str(raw_input('please input tieba url, delete the string behide pn=: \n'))  
begin_page = int(raw_input('please input begin page: \n'))
end_page = int(raw_input('please input end page: \n'))

baidu_tieba(bdurl, begin_page, end_page)