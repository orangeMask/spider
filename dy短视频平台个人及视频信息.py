# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/9/17  11:20
"""
import requests
import re
import json
from pool import *


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
	auth_dic = {}
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
	nickname = aweme_list[0]['author']['nickname']
	unique_id = aweme_list[0]['author']['unique_id']  # 自定义id
	signature = aweme_list[0]['author']['signature']  # 签名
	custom_verify = aweme_list[0]['author']['custom_verify']  # 头衔标签
	follower_count = aweme_list[0]['author']['follower_count']  # 他的粉丝数
	favoriting_count = aweme_list[0]['author']['favoriting_count']  # 他的关注数
	total_favorited = aweme_list[0]['author']['total_favorited']  # 总赞
	aweme_count = aweme_list[0]['author']['aweme_count']  # 视频数

	auth_dic['nickname'] = nickname
	auth_dic['unique_id'] = unique_id
	auth_dic['signature'] = signature
	auth_dic['desc'] = custom_verify.replace('\n', ' ')
	auth_dic['follow_count'] = follower_count
	auth_dic['fans_count'] = favoriting_count
	auth_dic['total_star'] = total_favorited
	auth_dic['video_count'] = aweme_count

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
	data_dic['auth'] = [auth_dic]
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
