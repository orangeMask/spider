# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/9/18  10:17
"""

from pool import *
import requests
from lxml import etree
import re
import json
from datetime import datetime


def html_get(url):
	headers = {
		'user-agent': get_ua(),
	}
	html = requests.get(url, headers)
	return html


def parse_click(top_time):
	url = f'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=week&top_cat=www_www_all_suda_suda&top_time={top_time}&top_show_num=50'
	html = html_get(url)
	data = re.findall('var data = (.*?);', html.text, re.S)[0]
	news_data = json.loads(data)
	click_news = news_data['data']
	return click_news


def parse_video(top_time):
	url = f'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=week&top_cat=video_news_all_by_vv&top_time={top_time}&top_show_num=50'
	html = html_get(url)
	data = re.findall('var data = (.*?);', html.text, re.S)[0]
	news_data = json.loads(data)
	video_news = news_data['data']
	return video_news


def parse_top():
	nowt = datetime.now().strftime('%Y%m%d')
	data = {
		'click_top': parse_click(nowt),
		'video_top': parse_video(nowt),
	}
	return json.dumps(data)


def parse_content(url):
	html = html_get(url)
	tree = etree.HTML(html.content.decode('utf-8'))
	title = tree.xpath('.//h1[@class="main-title"]/text()')[0]
	pubtime = tree.xpath('.//div[@id="top_bar"]//span[@class="date"]/text()')[0]
	nofollow = tree.xpath('.//div[@id="top_bar"]//a[@rel="nofollow"]/text()')[0]
	# print(title, pubtime, nofollow)
	img_list = tree.xpath('.//div[@id="article"]//img/@src')
	img_list = ['https:' + img for img in img_list]
	content_list = tree.xpath('.//div[@id="article"]/p/text()')
	content_list += img_list
	content = '\n'.join(content_list)
	data = {
		'title': title,
		'pubtime': pubtime,
		'nofollow': nofollow,
		'content': content,
		'img': img_list
	}
	return json.dumps(data)


if __name__ == '__main__':
	'''
	新闻榜单  parse_top,点击量,播放量
	单条新闻  parse_content
	'''
	print(parse_top())
	url = 'https://news.sina.com.cn/c/2020-09-18/doc-iivhvpwy7362635.shtml'
	# url = 'https://news.sina.com.cn/c/xl/2020-09-18/doc-iivhuipp5000766.shtml'
	print(parse_content(url))
