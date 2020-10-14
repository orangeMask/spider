# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/10/13  11:18
"""
import requests
import json
from pool import *


# 微热点

def html_get(url):
	headers = {
		'user-agent': get_ua(),
	}
	data = {
		'timeType': '1',
		'sort': '7',
		'page': '1',
		'pageSize': '100',
		'isLogin': 'false',
	}
	html = requests.post(url=url, headers=headers, data=data)
	return html.json()


url = 'https://www.wrd.cn/view/home/hotEvent/selectChooseListData.action'
# url = 'https://www.baidu.com'
print(html_get(url))
