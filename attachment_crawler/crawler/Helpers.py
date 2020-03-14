# -*- coding: utf-8 -*-

def is_url(url):
	# 没有判合法性，也可以用正则
	return url.startswith('www.') or url.startswith('http://') or url.startswith('https://')

def get_utf_8_str(i_str):
	if isinstance(i_str, unicode):
		return i_str.encode('utf-8')
	return i_str
