# -*- coding: utf-8 -*-

import os
import sys
import urllib2
import Helpers
from bs4 import BeautifulSoup  #用于解析网页

class AttachmentCrawler(object):
	# 定义爬虫类
	def __init__(self, dest_dir, raw_url, suffix=None):
		'''
		dest_dir: 文件下载子目录
		raw_url: 源地址
		suffix: # 感兴趣的附件后缀
		'''
		if suffix is None:
			self.interested_suffix = set(['pdf', 'doc', 'docx', 'xls', 'xlsx'])  # 感兴趣的附件后缀
		else:
			self.interested_suffix = set(suffix)
		self.dest_dir = dest_dir
		self.raw_url = raw_url
		self.raw_paths = raw_url.split('/')

	def get_absolute_path(self, href):
		if Helpers.is_url(href):
			return href
		paths = href.split('/')  # 理论上是xxx.pdf或../xx.pdf或../../xx.pdf这种
		parents = paths.count('..')
		if parents <= 0:  # 同一层级
			true_path = self.raw_paths[0:-1] + paths
		else:
			true_path = self.raw_paths[0:-parents-1] + [paths[-1]]
		return '/'.join(true_path)

	def download_attachment(self, file_url, file_name):
		# 下载，打印log，若目录不存在创建目录，原始文件存在先删除原文件？
		# print 'download_attachment:', file_url, file_name
		try:
			dest_path = os.path.join(self.dest_dir)
			if not os.path.exists(self.dest_dir):
				os.makedirs(self.dest_dir)
			file_path = os.path.join(self.dest_dir, file_name)
			if os.path.exists(file_path):  # 如果存在就不重复下了
				# print 'exists:', file_path
				return True
			u = urllib2.urlopen(file_url)
			f = open(file_path, 'wb')
			block_sz = 8192
			while True:
				buffer = u.read(block_sz)
				if not buffer:
					break

				f.write(buffer)
			f.close()
			print "Sucessful to download:", file_path
			return True
		except:
			sys.excepthook(*sys.exc_info())
			return False

	def run(self):
		failed_files, success_files = [], []
		suffix = self.raw_url.split('.')[-1]
		if suffix in self.interested_suffix:  # 原始url就是一个文件，直接下载
			file_name = self.raw_url.split('/')[-1]
			res = self.download_attachment(self.raw_url, file_name)
			if not res:
				failed_files.append(file_name)
			else:
				success_files.append(file_name)
		else:
			failed_files, success_files = self.parser_url_and_download_attachment()
		return failed_files, success_files

	def parser_url_and_download_attachment(self):
		html = urllib2.urlopen(self.raw_url)
		bsObj = BeautifulSoup(html, 'html.parser')
		hyperlink_tags = bsObj.find_all('a')  # 找到所有超链接tags, 超链接都是<a href=xxx>开始
		failed_files, success_files = [], []
		for tag in hyperlink_tags:
			name = tag.text.lstrip().rstrip()  # .text比.string要好,.text得到的是实际展示的内容(可能多个标签合并)，.string则只有在单标签时生效
			href = tag.get('href')
			if not href or not name:
				continue
			suffix = href.split('.')[-1]
			if suffix not in self.interested_suffix:
				continue
			file_url = self.get_absolute_path(href)
			if name.endswith(suffix):
				file_name = name
			else:
				file_name = name + '.' + suffix
			res = self.download_attachment(file_url, file_name)
			if not res:
				print 'download failed:', file_name
				failed_files.append(file_name)
			else:
				success_files.append(file_name)
		return failed_files, success_files



if __name__ == '__main__':
	raw_url = 'http://www.shenchunhui.com/_private/guifangxingwenjian/fagui/2020/pilujingxuanceng.htm'
	crawler = AttachmentCrawler('t1', raw_url)
	crawler.run()