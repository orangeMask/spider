# -*- encoding:utf-8 -*-
"""
@Auth：Jason
@Time：2020/9/17  11:20
"""
import datetime
import time
import requests
import re
import json
import hashlib
from pool import *


class TppComment(object):
	def __init__(self):
		self.appKey = "12574478"
		self.cookie2 = "115b197e8cca3ffeff588c0a37ad49e6"
		self.session = requests.session()
		self.url = 'https://acs.m.taopiaopiao.com/h5/mtop.film.mtopcommentapi.querytabshowcomments/7.0/'
		self.headers = {
			'user-agent': get_ua(),
		}

	def hash_md5(self, s):
		m = hashlib.md5()
		b = s.encode(encoding='utf-8')
		m.update(b)
		md5_s = m.hexdigest()
		return md5_s

	def session_get(self, showId, page):
		'''
		:param pageSize: 目前设置为20*page,
		:param page: 控制返回的数量
		:return:
		'''
		params = {
			'appKey': self.appKey,
		}
		cookie_jar = self.session.get(url=self.url, headers=self.headers, params=params).cookies
		cookie_dic = requests.utils.dict_from_cookiejar(cookie_jar)
		m_h5_tk = cookie_dic['_m_h5_tk']
		# m_h5_tk_enc = cookie_dic['_m_h5_tk_enc']
		tk, t = m_h5_tk.split('_')
		# cks = 'cookie2=115b197e8cca3ffeff588c0a37ad49e6' + '; _m_h5_tk=' + m_h5_tk + '; _m_h5_tk_enc=' + m_h5_tk_enc
		cookie_dic['cookie2'] = self.cookie2
		cookies = requests.cookies.cookiejar_from_dict(cookie_dic, cookiejar=None, overwrite=True)
		data_dic = {"type": 1, "tab": "NEW", "pageSize": 20 * page, "showId": showId, "cityCode": "110100",
		            "platform": "8"}
		data = json.dumps(data_dic)
		s = tk + "&" + t + "&" + self.appKey + "&" + data
		sign = self.hash_md5(s)
		params = {
			'appKey': self.appKey,
			't': t,
			'sign': sign,
			'data': data
		}
		data_js = self.session.get(url=self.url, headers=self.headers, params=params, cookies=cookies).json()
		return data_js

	def parse(self, movie_id, page):
		data_js = self.session_get(movie_id, page)
		comments = data_js['data']['returnValue']['comments']
		comments_list = []
		# now_stamp = int(time.time())
		for comment in comments:
			comment_dic = {}
			nickname = comment['nickName']
			comment_id = comment['id']
			remark = comment.get('remark')
			content = comment['content']
			commentTime = comment['commentTime']
			good = comment['favorCount']
			img = comment['avatar']
			img_flag = re.findall('^(i\d.*?)/', img)
			if img_flag:
				avatar = 'http://gw.alicdn.com/' + img
			else:
				avatar = 'http://gw.alicdn.com/tfs/TB1GJJtd2WG3KVjSZPcXXbkbXXa-180-180.png'
			# if remark:
			# 	star = float(remark) / 2
			# else:
			# 	star = ''
			time_stamp = int(commentTime)
			# if time_stamp - now_stamp > 60 * 15:
			# 	break
			date_array = datetime.datetime.utcfromtimestamp(time_stamp)
			time_com = date_array.strftime("%Y-%m-%d %H:%M:%S")
			comment_dic['user'] = nickname
			comment_dic['img'] = avatar
			comment_dic['comment'] = content
			comment_dic['comment_id'] = int(comment_id)
			comment_dic['remark'] = remark
			comment_dic['time'] = time_com
			comment_dic['good'] = ''.join(good)
			comments_list.append(comment_dic)
		return comments_list

	def manage_tpp(self, movie_id, pages):
		data_dic = {}
		comments_list = []
		# for i in range(pages):
		comments_list += self.parse(movie_id, int(pages))
		data_dic["comments"] = comments_list
		return json.dumps(data_dic, ensure_ascii=False)


if __name__ == '__main__':
	movie_url = 'https://dianying.taobao.com/showDetail.htm?spm=a1z21.6646273.w2.7.173a584fBe8prc&showId=1322282&n_s=new&source=current'
	movie_id = re.findall('.*?[taobao,taopiaopiao].*?show[i, I]d=([0-9]+).*?', movie_url)[0]
	pages = 1
	print(TppComment().manage_tpp(movie_id=movie_id, pages=pages))
