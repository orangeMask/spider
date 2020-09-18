# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/9/17  16:18
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


def parse_content(url):
	html = html_get(url)
	window_data = re.findall('window.DATA = (\{.*?\})', html.text, re.S)[0]
	win_data = json.loads(window_data)
	article_id = win_data['article_id']
	title = win_data['title']
	pubtime = win_data['pubtime']
	tags = win_data['tags']
	# print(article_id, title, pubtime, tags)
	# print(html.url)
	# print(html.text)
	tree = etree.HTML(html.text)
	p_list = tree.xpath('.//div[@class="content-article"]/p[@class="one-p"]')
	content_list = []
	for item in p_list:
		src = item.xpath('./img/@src')
		if src:
			text = 'http://' + src[0]
		else:
			text = item.xpath('./text()')[0]
		content_list.append(text)
	content = '\n'.join(content_list)
	data = {
		'article_id': article_id,
		'title': title,
		'pubtime': pubtime,
		'tags': tags,
		'content': content
	}
	return json.dumps(data)


def parse_importance():
	trpc = 'https://i.news.qq.com/trpc.qqnews_web.pc_base_srv.base_http_proxy/NinjaPageContentSync?pull_urls=news_top_2018'
	important_html = html_get(trpc).json()
	if important_html['msg'] == "success":
		important_news = important_html['data']
	else:
		important_news = ""
	return important_news


def parse_news_list():
	url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=24hours&srv_id=pc&offset=0&limit=20&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:7,%22check_type%22:true}'
	news_list_html = html_get(url).json()
	if news_list_html['msg'] == "success":
		hot_news = news_list_html['data']['list']
	else:
		hot_news = ""
	return hot_news


def parse_prevent():
	url = 'https://news.qq.com/ext2020/apub/json/prevent.new.json'
	prevent_html = html_get(url).json()
	for item in prevent_html:
		item['url'] = 'https://new.qq.com/rain/a/' + item['id']
	return prevent_html


def parse_top():
	data = {
		'important_news': parse_importance(),
		'prevent_news': parse_prevent(),
		'first_news': parse_news_list(),
	}
	return json.dumps(data)


if __name__ == '__main__':
	'''
	新闻榜单  parse_top 要闻榜11,热门25,首页20
	单条新闻  parse_content
	'''
	print(parse_top())
	url = 'https://new.qq.com/rain/a/20200917A0CJ3Q00'
	print(parse_content(url))
