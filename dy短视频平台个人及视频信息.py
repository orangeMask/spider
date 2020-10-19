# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/9/17  11:20
"""
import requests
import re
import json
from pool import *
from datetime import datetime
import time


# 个人主页信息

def switch_uid(url):
	headers = {
		'user-agent': get_ua(),
	}
	response = requests.get(url, headers)
	response_url = response.url
	uid = re.findall(r'/user/(\d+)', response_url)[0]
	# share_url = f'https://www.amemv.com/share/user/{uid}'
	return uid


def get_author(uid, put_cursor=''):
	video_list = []
	url = f'https://www.amemv.com/web/api/v2/aweme/post/?user_id={uid}'
	params = {
		'aid': '1128',
		'count': '21',
		'max_cursor': put_cursor
	}
	headers = {
		'user-agent': get_ua(),
	}
	html = requests.get(url=url, headers=headers, params=params)
	# print(html.text)
	response = html.json()
	extra_cursor = response['extra']['now']
	has_more = response['has_more']
	max_cursor = response['max_cursor']
	# print(extra_cursor, has_more, max_cursor)
	aweme_list = response['aweme_list']
	author = aweme_list[0]['author']
	nickname = author['nickname']
	avatar_larger = author['avatar_larger']['url_list']
	avatar_thumb = author['avatar_thumb']['url_list']
	avatar_medium = author['avatar_medium']['url_list']
	unique_id = author['unique_id']  # 抖音号自定义id
	signature = author['signature']  # 签名
	custom_verify = author['custom_verify']  # 头衔标签
	enterprise_verify_reason = author['enterprise_verify_reason']  # 认证
	follower_count = author['follower_count']  # 他的粉丝数
	favoriting_count = author['favoriting_count']  # 他的关注数
	total_favorited = author['total_favorited']  # 总赞
	aweme_count = author['aweme_count']  # 视频数
	cursor_now = datetime.fromtimestamp(extra_cursor / 1000)  # datetime格式时间
	cursor_time = cursor_now.strftime('%Y-%m-%d %H:%M:%S')
	# time.strftime('%Y-%m-%d %H:%M:%S', extra_cursor)
	auth_dic = {
		'cursor_now': cursor_time,
		'nickname': nickname,
		'unique_id': unique_id,
		'signature': signature,
		'desc': custom_verify.replace('\n', ' '),
		'verify': enterprise_verify_reason.replace('\n', ' '),
		'follower_count': follower_count,
		'fans_count': favoriting_count,
		'total_star': int(total_favorited),
		'video_count': aweme_count,
		'avatar_list': {
			'larger': avatar_larger[0],
			'medium': avatar_medium[0],
			'thumb': avatar_thumb[0]
		}  # 大中小头像
	}

	for aweme in aweme_list:
		statistics = aweme['statistics']
		desc = aweme['desc']
		text_extra = aweme['text_extra']
		if text_extra:
			name = text_extra[0]['hashtag_name']
		else:
			name = ''
		video_dic = {
			'video_name': name,
			'desc': desc,
		}
		video_dic.update(statistics)
		video_list.append(video_dic)
	return auth_dic, video_list, max_cursor, has_more


def get_aweme_info(uid, put_cursor=''):
	video_list = []
	url = f'https://www.amemv.com/web/api/v2/aweme/post/?user_id={uid}'
	params = {
		'aid': '1128',
		'count': '21',
		'max_cursor': put_cursor
	}
	headers = {
		'user-agent': get_ua(),
	}
	html = requests.get(url=url, headers=headers, params=params)
	# print(html.text)
	response = html.json()
	# extra_cursor = response['extra']['now']
	has_more = response['has_more']
	max_cursor = response['max_cursor']
	aweme_list = response['aweme_list']
	for aweme in aweme_list:
		video_dic = {}
		statistics = aweme['statistics']
		desc = aweme['desc']
		text_extra = aweme['text_extra']
		if text_extra:
			name = text_extra[0]['hashtag_name']
		else:
			name = ''
		video_dic['video_name'] = name
		video_dic['desc'] = desc
		video_dic.update(statistics)
		video_list.append(video_dic)
	return video_list, max_cursor, has_more


def manage_dy(url, page=1):
	'''
	:param url: 分享页链接
	:return:
			switch_uid: 请求获取数字uid
			get_author: 获取用户信息及视频信息  # 每个视频信息下有发布用户信息,采用第一个视频的用户信息
			get_aweme_info: 获取视频信息
	'''
	data_dic = {}
	uid = switch_uid(url)
	auth_dic, video_list, max_cursor, has_more = get_author(uid)
	if has_more:
		for i in range(page):
			v_list, max_cursor, has_more = get_aweme_info(uid, put_cursor=max_cursor)
			video_list += v_list
			if has_more:
				continue
			else:
				break
	else:
		pass
	data_dic['auth'] = auth_dic
	data_dic['video'] = video_list
	return json.dumps(data_dic)


if __name__ == '__main__':
	'''
	page  页数，一页20条视频信息
	text  主页分享的用户信息  例：'在，记录美好生活！ https://v.douyin.com/JS3gbyE/'
	'''
	page = 1  # 页数
	text = '在，记录美好生活！ https://v.douyin.com/JS3gbyE/'  # 四川观察
	dy_id = re.findall(r'https://v.douyin.com/(\w+)', text)[0]  # 正则获取JS3gbyE
	url = 'https://v.douyin.com/' + dy_id
	# print(url)
	# print(manage_dy(url))
	print(manage_dy(url, page))
