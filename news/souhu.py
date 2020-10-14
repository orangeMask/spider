# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/9/22  14:56
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
	url = 'https://www.sohu.com/'
	html = html_get(url)
	tree = etree.HTML(html.text)
	item_list = tree.xpath('.//div[@class="focus-news-box"]/div[not (@id="entrance")]//a')
	data_list = []
	for i in item_list:
		url = i.xpath('./@href')[0]
		title = i.xpath('./@title')[0]
		data_list.append({'url': url, 'title': title})
	data = {'focus_news': data_list}
	return json.dumps(data)


def parse_content(url):
	html = html_get(url)
	tree = etree.HTML(html.text)
	href = tree.xpath('.//link[@rel="canonical"]/@href')[0]
	tags = tree.xpath('.//meta[@name="keywords"]/@content')[0]
	title = tree.xpath('.//div[@class="text-title"]/h1/text()')[0].strip()
	pubtime = tree.xpath('.//span[@id="news-time"]/text()')[0]
	auth = tree.xpath('.//div[@class="text-title"]/div/span[2]/a/text()')[0]
	p_list = tree.xpath('.//article[@id="mp-editor"]/p')
	content_list = []
	for item in p_list:
		img = item.xpath('./img/@src')
		if img:
			text = img[0]
		else:
			text = ''.join(item.xpath('.//text()')).strip()
		content_list.append(text)
	# print(content_list)
	# t = tree.xpath('.//article[@id="mp-editor"]/p[last()]/span/text()')
	content = '\n'.join(content_list)
	data = {
		# 'href': href,
		'title': title,
		'pubtime': pubtime,
		'auth': auth,
		'tags': tags,
		'content': content
	}
	return json.dumps(data)


if __name__ == '__main__':
	print(parse_top())
	url = "https://www.sohu.com/a/420028936_100237836"
	print(parse_content(url))
