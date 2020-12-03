# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 14:19
# @Author  : Jason
# Python3.8

import requests
import re
import json
from pool import *
from datetime import datetime
import time


def html_get(uid):
	url = "https://live.kuaishou.com/m_graphql"
	headers = {
		'Host': 'live.kuaishou.com',
		'Origin': 'https://live.kuaishou.com',
		'Referer': f'https://video.kuaishou.com/profile/{uid}',
		'User-Agent': get_ua(),
		'Cookie': ''
	}
	cookie_like = "你的登陆cookie"
	headers["Cookie"] = cookie_like
	data = {"operationName": "visionProfilePhotoList", "variables": {"userId": f"{uid}", "pcursor": "1.6065432E12"},
	        "query": "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page) {\n    result\n    llsid\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        expTag\n        __typename\n      }\n      canAddComment\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"}
	html = requests.post(url, headers=headers, json=data)
	response = html.json()
	print(html.content.decode('utf8'))
	return response


uid = "3x47r4fmcw2bey4"
# uid = "3xxjfdbpd5ppshm"
html_get(uid=uid)

# url = "https://live.kuaishou.com/profile/3x47r4fmcw2bey4"
# url = "https://v.kuaishou.com/8Z1qM7"
# headers = {
# 	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Aoyou/VlhrXg15dyYJNFckS3pKR_yYMnCicnIf4-0PoDM_GCi7Ss3u2dR6557fvw==",
# }
# html = requests.get(url=url, headers=headers)
# print(html)
# print(html.content.decode('utf8'))
# print(html.url)


# if __name__ == '__main__':
#     "看了这么多快手，还是「虎哥说车」最好玩了！ https://v.kuaishou.com/8Z1qM7 复制此消息，打开【快手】直接观看！"
