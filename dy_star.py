# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/10/13  13:28
"""
from pool import *
import requests
import json
from retrying import retry


# 明星榜

@retry()
def html_get(url):
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Aoyou/UChwWVlBMWJmc15PSitcWE9-sif3-0nKQ9OdtLHQ2QbAXUxr6oeIK1znvg=='
	}
	html = requests.get(url=url, headers=headers)
	return html


def parse(html):
	data_json = html.json()
	active_time = data_json['active_time']  # 更新时间
	user_list = data_json['user_list']
	users_info = []
	for item in user_list:
		hot_value = item['hot_value']
		hot_value_bar = item['hot_value_bar']
		factor_hot_value = item['factor_hot_value']
		factor_interact_value = item['factor_interact_value']

		user_info = item['user_info']
		signature = user_info['signature']
		sec_uid = user_info['sec_uid']
		uid = user_info['uid']
		nickname = user_info['nickname']
		avatar_thumb = user_info['avatar_thumb']['url_list'][0]
		avatar_larger = user_info['avatar_larger']['url_list'][0]
		data_info = {
			"user_info": {
				'nickname': nickname,
				'signature': signature,
				'uid': uid,
				'sec_uid': sec_uid,
				'avatar_thumb': avatar_thumb,
				'avatar_larger': avatar_larger,
			},
			"hots": {
				'hot_value': hot_value,
				'hot_value_bar': hot_value_bar,
				'factor_hot_value': factor_hot_value,
				'factor_interact_value': factor_interact_value,
			}
		}
		users_info.append(data_info)
	data = {
		'active_time': active_time,
		'users_info': users_info,
	}
	return data


def manage():
	url = 'https://aweme.snssdk.com/aweme/v1/hotsearch/star/billboard/'
	html = html_get(url)
	data = parse(html)
	return json.dumps(data)


if __name__ == '__main__':
	print(manage())
