# -*- coding: utf-8 -*-  
#---------------------------------------  
#   程序：thinkjs.org爬虫  
#   语言：Python 2.7   
#   作者：jiao.shen
#   github: http://github.com/wangasi
#   功能：将thinkjs使用文档html页面存储到本地。  
#   操作：先获得各级网页的路径，然后下载网页内容，过滤后存储到本地
#---------------------------------------  

import scrapy
from weather.items import WeatherItem

class WeatherSpider(scrapy.Spider):
	name = 'myweather'
	allowed_domains = ['sina.com.cn']
	start_urls = ['http://weather.sina.com.cn/']

	def  parse(self, response):
		item = WeatherItem()
		item['city'] = response.xpath('//*[@id="slider_ct_name"]/text()').extract()
		tenDay = response.xpath('//*[@id="blk_fc_c0_scroll"]')
		item['date'] = tenDay.css('p.wt_fc_c0_i_date::text').extract()
		item['dayDesc'] = tenDay.css('img.icons0_wt::attr(title)').extract()
		item['dayTemp'] = tenDay.css('p.wt_fc_c0_i_temp::text').extract()

		return item
		