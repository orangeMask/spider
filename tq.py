# -*- coding: utf-8 -*-
# @Time    : 2020/12/2 13:48
# @Author  : Jason
# Python3.8
from pool import *
import requests
import re
from lxml import etree
import json


def html_get(code, f=None):
	# url = f"http://forecast.weather.com.cn/town/weather1dn/{code}.shtml"
	if f:
		url = f"http://forecast.weather.com.cn/town/weathern/{code}.shtml"
	else:
		url = f"http://www.weather.com.cn/weather/{code}.shtml"
	headers = {
		"User-Agent": get_ua(),
	}
	html = requests.get(url=url, headers=headers)
	return html.content.decode('utf8')


def parse(response):
	tree = etree.HTML(response)
	li_list = tree.xpath('.//div[@id="7d"]/ul/li')
	seven_list = []
	for li in li_list:
		day = li.xpath('./h1/text()')
		wea = li.xpath('./p[1]/text()')
		tem = li.xpath('./p[@class="tem"]//text()')
		win = li.xpath('./p[@class="win"]//text()')
		day = ''.join(day).replace('\n', '')
		wea = ''.join(wea).replace('\n', '')
		tem = ''.join(tem).replace('\n', '')
		win = ''.join(win).replace('\n', '')
		one_day = {
			"day": day,
			"wea": wea,
			"tem": tem,
			"win": win,
		}
		seven_list.append(one_day)
	return seven_list


def parse2(response):
	tree = etree.HTML(response)
	dates_list = tree.xpath('.//ul[@class="date-container"]/li')

	li_list = tree.xpath('.//ul[@class="blue-container backccc"]/li')
	seven_list = []
	i = 0
	for li in li_list[0:-1]:
		day = dates_list[i].xpath('.//text()')
		day = ''.join(day).strip()
		wea_day = li.xpath('./i[1]/@title')
		wea_night = li.xpath('./i[1]/@title')
		wea = li.xpath('./p[1]/text()')
		wind_day = li.xpath('./div[@class="wind-container"]/i[1]/@title')
		wind_night = li.xpath('./div[@class="wind-container"]/i[2]/@title')
		win = li.xpath('./p[@class="wind-info  info-style"]/text()')
		wea_day = ''.join(wea_day).strip()
		wea_night = ''.join(wea_night).strip()
		wea = ''.join(wea).strip()
		wind_day = ''.join(wind_day).strip()
		wind_night = ''.join(wind_night).strip()
		win = ''.join(win).strip()
		i += 1
		one_day = {
			"day": day,
			"wea": {
				"day": wea_day,
				"night": wea_night,
				"wea": wea,
			},
			"win": {
				"day": wind_day,
				"night": wind_night,
				"power": win,
			},
		}
		seven_list.append(one_day)
	return seven_list


def manage(search):
	city_url = f"http://toy1.weather.com.cn/search?cityname={search}"
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
	}
	response = requests.get(url=city_url, headers=headers).content.decode('utf8')
	# result = re.findall('"([a-zA-Z0-9]+)~[a-z]+~(.*?)~.*?~(.*?)"', response)
	result = re.findall('"([0-9]{9})~[a-z]+~(.*?)~.*?~([\\u4E00-\\u9FA5]+)"', response)
	cities_wea = []
	for item in result:
		code = item[0]
		name = f"{item[2]} {item[1]}"
		# print(code, name)
		try:
			res = html_get(code)
			one_city = parse(res)
		except:
			"""没有温度"""
			res = html_get(code, f=2)
			one_city = parse2(res)
		item_dic = {
			"name": name,
			"weather": one_city
		}
		cities_wea.append(item_dic)
	print(json.dumps(cities_wea, ensure_ascii=False))
	return json.dumps(cities_wea)


if __name__ == '__main__':
	search = "cs"
	manage(search)
