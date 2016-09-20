import urllib
import urllib2 

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
top_level_url = 'http://example.com/foo/'
password_mgr.add_password(None, top_level_url,'why', '1223') 
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)
a_url = 'http://www.baidu.com/'
opener.open(a_url) 
urllib2.install_opener(opener) 


'''
old_url = 'http://www.baidu.com'
req = Request(old_url)
respone = urlopen(req)
print respone.info()


url = 'http://ndapi.bestinfoods.com/market/get/ad'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {
	'classId' : '1',
	'type' : '1'}

headers = { 'User-Agent' : user_agent }
data = urllib.urlencode(values)

req = urllib2.Request(url, data, headers)
try: respone = urllib2.urlopen(req)
except urllib2.URLError, e:
	print e.reason

html = respone.read()
print html
'''

'''
req = Request('http://bbs.csdn.net/callmewhy')
try: respone = urlopen(req)

except URLError, e:    
  
    if hasattr(e, 'code'):    
    
        print 'The server couldn\'t fulfill the request.'    
    
        print 'Error code: ', e.code    
  
    elif hasattr(e, 'reason'):    
    
        print 'We failed to reach a server.'    
    
        print 'Reason: ', e.reason   

else:
	print 'No exception was raised.'
'''

'''
old_url = 'http://rrurl.cn/b1UZuP'
req = Request(old_url)
respone = urlopen(req)
print 'Old url : ' + old_url
print 'Real url : ' + respone.geturl()
'''