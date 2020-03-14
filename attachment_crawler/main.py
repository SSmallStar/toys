# -*- coding: utf-8 -*-

import os
import sys
import time
import crawler.ExcelParser as ExcelParser
import crawler.AttachmentCrawler as AttachmentCrawler
import crawler.Helpers as Helpers


def download_excel_attachment(excel_file):
	'''
	附件下载爬虫说明
	1.默认认为excel文件中每张子表的每一行中有一个编号+一个url
	2.按sheet子表名/编号/的结构，下载附件
	3.程序执行完毕，若有下载失败的文件或url，会输出到failed_时间.log里
	'''
	excel_parser = ExcelParser.ExcelParser(excel_file)
	data = excel_parser.load_excel()
	all_failed_files = []
	failed_urls = []
	for sheet_name, sheet_data in data.iteritems():
		u_sheet_name = Helpers.get_utf_8_str(sheet_name)
		for index, url in sheet_data.iteritems():
			index = str(index)
			url = Helpers.get_utf_8_str(url)
			try:
				dir_path = os.path.join('download', sheet_name, index)
				print 'processing:%s - %s - %s' % (sheet_name, index, url)
				crawler = AttachmentCrawler.AttachmentCrawler(dir_path, url)
				failed_files, success_files = crawler.run()
				for f in failed_files:
					all_failed_files.append((u_sheet_name, index, f, url))
				if not success_files and not all_failed_files:
					failed_urls.append((u_sheet_name, index, '未发现附件', url))
			except:
				sys.excepthook(*sys.exc_info())
				print '%s-%s-%s download failed' % (sheet_name, index, url)
				failed_urls.append((u_sheet_name, index, url))

	if failed_urls or failed_files:
		time_str = time.strftime('%Y_%m_%d_%H_%M_%S')
		log_name = 'failed_%s.log' % time_str
		with open(log_name, 'wb') as f:
			f.write('-------------下载失败的url---------------\n')
			for f_url in failed_urls:
				info = ' '.join(f_url)
				f.write(info+'\n')

			f.write('-------------下载失败的文件-------------\n')
			for f_f in all_failed_files:
				info = ' '.join(f_f)
				f.write(info+'\n')
			print u'失败日志已写入:', log_name

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print u'请将excel文件作为参数传入'
		sys.exit(1)
	# excel_name = u'有关法规系列（30） - 20200311.xlsx'
	excel_name = sys.argv[1]
	download_excel_attachment(excel_name)