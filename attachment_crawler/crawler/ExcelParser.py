# -*- coding: utf-8 -*-

import os
import sys
import xlrd
import Helpers

excel_name = ''


def is_url(url):
	# 没有判合法性，也可以用正则
	return url.startswith('www.') or url.startswith('http://') or url.startswith('https://')

class ExcelParser(object):
	def __init__(self, excel_name):
		self.excel_name = excel_name

	def load_sheet_data_to_dict(self, sheet):
		count = 0
		data = {}
		for i in range(sheet.nrows):
			row = sheet.row(i)
			index, url = None, None
			for idx, cell in enumerate(row):  # 这里只处理一行中有一个编号(数字)+一个url的情况
				# print idx, cell, cell.ctype == xlrd.XL_CELL_NUMBER
				if index is None and cell.ctype == xlrd.XL_CELL_NUMBER:
					index = int(cell.value)
				elif url is None and cell.ctype == xlrd.XL_CELL_TEXT:
					if Helpers.is_url(cell.value):
						url = cell.value
				if index is not None and url:
					data[index] = url
					break
		return data

	def load_excel(self):
		xl_book = xlrd.open_workbook(self.excel_name)
		print type(xl_book), xl_book
		sheets = xl_book.sheets()
		excel_data = {}
		for sheet in sheets:
			data = self.load_sheet_data_to_dict(sheet)
			if data:
				excel_data[sheet.name] = data
				print sheet.name, len(data)
			else:
				print '%s has no data' % sheet.name
		return excel_data

if __name__ == '__main__':
	excel_parser = ExcelParser(u'../有关法规系列（30） - 20200311.xlsx')
	data = excel_parser.load_excel()
	print '-------------------------------------'
	from pprint import pprint
	pprint(data)
	print '-------------------------------------'
