# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/9/17  11:20
"""
from pool import *
import requests
import json
import time
import re
import hashlib
from retrying import retry


def h_md5(s):
	m = hashlib.md5()
	b = s.encode(encoding='utf-8')
	m.update(b)
	md5_s = m.hexdigest()
	return md5_s


def get_cookie():
	url = 'https://acs.m.taopiaopiao.com/h5/mtop.film.mtopshowapi.getuserscorebyshowid/6.9/?appKey=12574478'
	headers = {
		'user-agent': get_ua(),
	}
	response = requests.get(url=url, headers=headers)
	ck = response.cookies
	m_h5_tk = ck['_m_h5_tk']
	m_h5_tk_enc = ck['_m_h5_tk_enc']
	tk, t = m_h5_tk.split('_')
	cks = 'cookie2=115b197e8cca3ffeff588c0a37ad49e6' + '; _m_h5_tk=' + m_h5_tk + '; _m_h5_tk_enc=' + m_h5_tk_enc
	return tk, t, cks


@retry(stop_max_attempt_number=3)
def get_point(movie_id):
	# url = 'https://acs.m.taopiaopiao.com/h5/mtop.film.mtopshowapi.getuserscorebyshowid/6.9'
	url = 'https://acs.m.taopiaopiao.com/h5/mtop.film.mtopshowapi.getextendshowbyid/5.4/'
	tk, t, cks = get_cookie()
	appKey = "12574478"
	# data_dic = {"showId": movie_id, "platform": "8"}
	data_dic = {"showid": movie_id, "cityCode": "110100", "platform": "8"}
	data = json.dumps(data_dic)
	s = tk + "&" + t + "&" + appKey + "&" + data
	sign = h_md5(s)
	params = {
		'appKey': appKey,
		't': t,
		'sign': sign,
		'data': data,
	}
	cookies = {'cookies': cks}
	headers = {
		'user-agent': get_ua(),
	}
	resp = requests.get(url=url, headers=headers, params=params, cookies=cookies)
	return resp


def parse_tpp(movie_id):
	html = get_point(movie_id)
	response = html.json()
	ret = response.get('ret')
	movie_dic = {}
	if "成功" in ''.join(ret):
		return_value = response['data']['returnValue']
		avatar = return_value['poster']
		category = return_value['type']
		cate = category.split(',')
		timing_length = return_value['duration']
		released_area = return_value['country']
		released_time = return_value['openTime']
		name = return_value['showName']
		score_list = return_value.get('scoreDataList')
		point = return_value.get('remark')
		wish_num = return_value['scoreAndFavor']['favorCount']
		# show_guide = return_value['showGuide']
		if point:
			one_star = score_list[4]['score']
			two_star = score_list[3]['score']
			three_star = score_list[2]['score']
			four_star = score_list[1]['score']
			five_star = score_list[0]['score']
			# tag_list = return_value['tagList']
			# show_sub_guide = return_value['showSubGuide']
			people = return_value['remarkCount']
			watched_num = return_value['scoreAndFavor']['watchCount']
		# wish_num = return_value['scoreAndFavor']['favorCount']
		else:
			point = ""
			people = ""
			watched_num = ""
			# wish_num = ""
			one_star = ""
			two_star = ""
			three_star = ""
			four_star = ""
			five_star = ""
		# tags = []
		movie_dic["name"] = name
		movie_dic['avatar'] = 'http://gw.alicdn.com/' + avatar
		movie_dic['category'] = cate
		movie_dic['released_area'] = released_area
		movie_dic['timing_length'] = timing_length
		movie_dic['released_time'] = released_time
		movie_dic["point"] = point
		movie_dic["people"] = people
		movie_dic["watched"] = watched_num
		movie_dic["wish"] = wish_num
		movie_dic["one_star"] = one_star
		movie_dic["two_star"] = two_star
		movie_dic["three_star"] = three_star
		movie_dic["four_star"] = four_star
		movie_dic["five_star"] = five_star
	# movie_dic["tags"] = tags
	else:
		movie_dic = {}
	return movie_dic


def manage_tpp_point(movie_id):
	data_dic = parse_tpp(movie_id=movie_id)
	data_dic["movie_id"] = movie_id
	return json.dumps(data_dic, ensure_ascii=False)


if __name__ == '__main__':
	movie_url = 'https://dianying.taobao.com/showDetail.htm?spm=a1z21.6646273.w2.7.173a584fBe8prc&showId=1322282&n_s=new&source=current'
	movie_id = re.findall('.*?[taobao,taopiaopiao].*?show[i, I]d=([0-9]+).*?', movie_url)[0]
	print(manage_tpp_point(movie_id=movie_id))
