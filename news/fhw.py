# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/9/21  10:22
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


def parse_top_title(content):
	data_list = []
	if isinstance(content, list):
		for item in content:
			children = item['children']
			if children:
				if isinstance(children, list):
					# print('chi', children)
					# url = children[0]['url']
					# title = children[0]['title'] + item['title']
					data_one = children[0]
				else:
					# url = children['url']
					# title = children['title'] + item['title']
					children.update({'title': children['title'] + item['title']})
					data_one = children
			else:
				# url = item['url']
				# title = item['title']
				item.pop('children')
				data_one = item
			data_list.append(data_one)
	else:
		children = content['children']
		data_list = children
		if children:
			# url = children['url']
			# title = children['title'] + content['title']
			children.update({'title': children['title'] + content['title']})
			data_one = children
		else:
			# url = content['url']
			# title = content['title']
			content.pop('children')
			data_one = content
		# print(url, title)
		data_list.append(data_one)
	return data_list


def parse_top():
	url = "https://www.ifeng.com/"
	html = html_get(url)
	response = html.text.replace(' ', '')
	all_data = re.findall('varallData=(\{.*?"isIpad":.*?});', response, re.S)[0]
	all_data = json.loads(all_data)
	news_content_0 = all_data['newsContent0']
	news_content_1 = all_data['newsContent1']
	data0 = parse_top_title(news_content_0)
	data1 = parse_top_title(news_content_1)
	data_list = data0 + data1
	data = {"ifeng_news": data_list}
	return json.dumps(data)


def parse_content(url):
	html = html_get(url)
	tree = etree.HTML(html.text)
	tags = tree.xpath('.//meta[@name="keywords"]/@content')[0]
	title = tree.xpath('.//div[@id="root"]/div[1]/div[2]/div[1]/h1/text()')[0]
	pubtime = tree.xpath('.//div[@id="root"]/div[1]/div[2]/div[1]/p/span/text()')[0]
	auth = tree.xpath('.//div[@id="root"]/div[1]/div[2]/div[1]/p/span/a/text()')[0]
	# print(title, pubtime, auth)
	p_list = tree.xpath('.//div[@id="root"]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/p')
	content_list = []
	for item in p_list:
		img = item.xpath('./img/@src')
		if img:
			text = img[0]
		else:
			text = item.xpath('.//text()')[0]
		content_list.append(text)
	content = '\n'.join(content_list)
	data = {
		'title': title,
		'pubtime': pubtime,
		'auth': auth,
		'tags': tags,
		'content': content
	}
	return json.dumps(data)


if __name__ == '__main__':
	'''
	新闻榜单  parse_top 要闻榜27
	单条新闻  parse_content
	'''
	print(parse_top())
	url = 'https://news.ifeng.com/c/7zutAzvEQTI'
	print(parse_content(url))
