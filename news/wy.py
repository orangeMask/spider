# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/9/17  17:26
"""
from pool import *
import requests
from lxml import etree
import re
import json


def html_get(url):
	headers = {
		'user-agent': get_ua(),
	}
	html = requests.get(url, headers)
	return html


def parse_top():
	url = 'https://news.163.com/rank/'
	html = html_get(url)
	tree = etree.HTML(html.text)
	item_list = tree.xpath(
		'.//div[@class="area areabg1"]/div[@class="area-half left"][1]/div/div[not (@class="title-tab")]')
	data = {}
	for i in range(len(item_list)):
		data_list = []
		item = item_list[i]
		tr_list = item.xpath('./table/tr')
		flag = 0
		for tr in tr_list:
			if flag:
				href = tr.xpath('./td[1]/a/@href')[0]
				title = tr.xpath('./td[1]/a/text()')[0]
				click = tr.xpath('./td[2]/text()')[0]
				news_data = {'title': title, 'url': href, 'click': click}
				data_list.append(news_data)
			# print(title, href, click)
			else:
				flag += 1
				continue
		if i == 0:
			# hour_news = data_list
			data['hour_news'] = data_list
		elif i == 1:
			# day_news = data_list
			data['day_news'] = data_list
		else:
			# week_news = data_list
			data['week_news'] = data_list
	return json.dumps(data)


def parse_content(url):
	html = html_get(url)
	tree = etree.HTML(html.text)
	title = tree.xpath('.//div[@id="epContentLeft"]/h1/text()')[0]
	tags = tree.xpath('.//meta[@name="keywords"]/@content')
	# pubtime = tree.xpath('./html[@id="ne_wrap"]/@data-publishtime')
	pubtime = re.findall('data-publishtime="(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})">', html.text, re.S)[0]
	p_list = tree.xpath('.//div[@id="endText"]/p')
	content_list = []
	for p in p_list:
		src = p.xpath('./img/@src')
		con = p.xpath('.//text()')
		if src:
			text = src[0]
		elif con:
			text = con[0].replace('\n', '').strip()
		else:
			text = ''
		content_list.append(text)
	content = '\n'.join(content_list)
	data = {

		'title': title,
		'pubtime': pubtime,
		'tags': tags,
		'content': content
	}
	return json.dumps(data)


if __name__ == '__main__':
	'''
	新闻榜单  parse_top 一小时点击量10,二十小时点击量10,七天点击量10
	单条新闻  parse_content
	'''
	print(parse_top())
	url = 'https://news.163.com/20/0917/20/FMOLF6RN0001899O.html'
	print(parse_content(url))

