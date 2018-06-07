# -*- coding: utf-8 -*-


from matplotlib.font_manager import *  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyautogui
import xlrd
import xlwt
import sys
import csv
import os
import collections
import seaborn as sns
from pylab import *
import copy
# plt.style.use('seaborn') #使用seaborn画图风格

#-----------------------------------------------------------------------------------------------
def matmul(ty, tx, tz):#矩阵乘法
	tablex = np.mat(tx.ix[tz,tx.columns])
	tabley = np.mat(ty.iloc[0])
	tablexy = tabley*tablex
	return tablexy

def fact(n, lt):#递归加
	if n==0:
		return lt[0]
	return lt[n]+fact(n-1, lt)

def parse_table(file_input, sheetindex):#读取excel表格，并转化为pd.dataframe
	workbook = xlrd.open_workbook(file_input)
	sheet = workbook.sheet_by_index(sheetindex)
	table = pd.read_excel(file_input, sheetname=sheet.name, usecols=range(0,sheet.ncols), skiprows=[0,2], skip_footer=0, index_col=[0], header=0)
	return table

def get_table_head(file_input, sheetindex):#得到表头，为得到stage和chara做准备
	workbook = xlrd.open_workbook(file_input)
	sheet = workbook.sheet_by_index(sheetindex) #资源采集清单系数（每kg）数据库提取参数
	table_row = pd.read_excel(file_input, sheetname=sheet.name).shape[0]
	return pd.read_excel(file_input, sheetname=sheet.name, usecols=range(0,sheet.ncols),  skip_footer=table_row-2, index_col=[0], header=0)

def get_Head_numlist(table):#得到stage的计数列表
	counter_Stage_col = 0 
	counter_stage_row = 1
	stage_collist = []
	for col in table.columns:
		if "Unnamed" not in col:
			counter_stage_row += 1
			stage_collist.append(counter_Stage_col)
			counter_Stage_col = 0
		counter_Stage_col += 1
		if counter_Stage_col ==0:
			Stage1.append(table.ix[1,col])
	stage_collist.append(counter_Stage_col)
	stage_row = counter_stage_row-1

	stage_numlist = []
	for i in range(len(stage_collist)):
		stage_numlist.append(fact(i,stage_collist))
	return stage_row, stage_numlist

def get_list_head(table_head_stage, table_head_chara, stage_row, stage_numlist, chara_row, chara_numlist):	# 求得表头计数列表
	list_stage_head = []
	list_stage_head_lable = []
	list_chara_head = []
	list_chara_head_lable = []
	for row in range(stage_row):#求阶段Stage表头计数列表 
		list_stage_head.append(table_head_stage.ix[0,range(stage_numlist[row],stage_numlist[row+1])])
		table_head_stage.ix[0,range(stage_numlist[row],stage_numlist[row+1])] = table_head_stage.ix[0,range(stage_numlist[row],stage_numlist[row+1])] + "_"+table_head_stage.columns[stage_numlist[row]]
		list_stage_head_lable.append(table_head_stage.ix[0,range(stage_numlist[row],stage_numlist[row+1])])
	for row in range(chara_row):#求特征化Chara表头计数列表
		list_chara_head.append(table_head_chara.ix[0,range(chara_numlist[row],chara_numlist[row+1])])
		table_head_chara.ix[0,range(chara_numlist[row],chara_numlist[row+1])] = table_head_chara.ix[0,range(chara_numlist[row],chara_numlist[row+1])] + "_"+table_head_chara.columns[chara_numlist[row]]
		list_chara_head_lable.append(table_head_chara.ix[0,range(chara_numlist[row],chara_numlist[row+1])])
	return list_stage_head, list_stage_head_lable, list_chara_head, list_chara_head_lable

def get_table_res_lable(file_input, list_stage_head_lable):
	list_stage_head_inone = []
	table_res_lable = parse_table(file_input,0)
	for layer1 in range(len(list_stage_head_lable)):
		for layer2 in range(len(list_stage_head_lable[layer1])):
			list_stage_head_inone.append(list_stage_head_lable[layer1][layer2])
	table_res_lable.columns = list_stage_head_inone
	return table_res_lable

def get_table_chara_lable(file_input, list_chara_head_lable):
	list_chara_head_inone = []
	table_chara_lable = parse_table(file_input,1)
	for layer1 in range(len(list_chara_head_lable)):
		for layer2 in range(len(list_chara_head_lable[layer1])):
			list_chara_head_inone.append(list_chara_head_lable[layer1][layer2])
	table_chara_lable.columns = list_chara_head_inone
	return table_chara_lable

def get_epd(product_num, table_head_stage, table_head_chara, list_stage_head_lable, list_chara_head, list_chara_head_lable, table_res_lable, table_chara_lable): # 求特制化结果
	# table_res_lable = table_res_lable
	table_total = []
	table_result = []
	table_mul = []

	# 求实际使用物质转换矩阵table_mul-----------------------------------------
	for num in range(product_num): 
		table_mul.append(table_res_lable*table_res_lable.iloc[-(product_num-num)])
		# table_mul.append(table_res_lable*table_res_lable.iloc[-(product_num*2-2*num-1)])#如果是t和m2间隔（-9,-7,-5,-3,-1）
		table_mul[num].drop(table_mul[num].index[range(-1,-product_num-1,-1)],inplace=True)

	# 求各阶段之和矩阵table_total-----------------------------------------
	for num in range(product_num):
		table_total.append(pd.DataFrame())

	for num in range(product_num):
		counter = 0
		for col in table_head_stage.columns:
			if "Unnamed" not in col:
				table_total[num][col] = table_mul[num][list_stage_head_lable[counter]].sum(axis=1)
				counter += 1
	
	# 求特制化结果矩阵table_result-----------------------------------------
	for num in range(product_num):
		get_result_t = []
		get_result_m2 = []
		table_result_index = []
		counter = 0

		for col in table_head_chara.columns:
			if "Unnamed" not in col:
				get_result_t.append(list(pd.DataFrame(matmul(table_chara_lable[list_chara_head_lable[counter]], table_total[num], list_chara_head[counter])).iloc[0]))
				table_result_index.append(col) #求特征化index
				counter += 1
		table_result.append(pd.DataFrame(get_result_t, index=table_result_index))
		table_result[num].columns = table_total[num].columns

	writer = pd.ExcelWriter('result.xlsx') # 导出excel
	table_result[0].to_excel(writer,'燃气灶')
	writer.save()

	return table_mul, table_total, table_result

def csv_export(csvfile_name, fieldnames, data):
	with open(csvfile_name, 'w', newline='') as csvfile: #Ubuntu
	# with open(csvfile_name, 'w', encoding='UTF8', newline='') as csvfile: #windows
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(data)

def get_csv(file_input, file_result, unit_field):

	field = ['product', 'stage', 'chara', 'result', 'unit']
	get_dict = collections.defaultdict()
	get_list = []
	workbook = xlrd.open_workbook(file_result)
	for sheet in workbook.sheet_names():
		data_xls = pd.read_excel(file_result, sheet, index_col = 0)
		for col in data_xls:
			counter = 0
			for data in data_xls[col]:
				get_dict = {'product': sheet, 'stage': col, 'chara': data_xls.index[counter],  'unit':unit_field['%s'%(data_xls.index[counter])] , 'result': data}
				get_list.append(get_dict)
				counter += 1
	csv_export("result.csv",field, get_list)

def get_sens_table_res_lable(file_input, list_stage_head_lable, table_res_lable, product_num, delta_x):#求敏感度变化delta_x的数列
	sens_table_res_lable = []
	trl_raw = copy.deepcopy(table_res_lable)

	for ind, tab in enumerate(table_res_lable.iloc[-1]):
		trl_copy = copy.deepcopy(table_res_lable.iloc[-1])
		trl_copy[ind]=tab*(1+delta_x) #原始数据增加10%
		trl_raw.iloc[-1] = trl_copy
		trl_raw_copy = copy.deepcopy(trl_raw)
		sens_table_res_lable.append(trl_raw_copy)

	return sens_table_res_lable

def senstivity(Mrow, Mnew, dx):# 求敏感度
	return (Mnew - Mrow)/Mrow/dx

def sens_plot(sens_result, title):# 画图
	x = sens_result.columns
	y = sens_result.index
	width = 0.0
	idx = np.arange(len(x))
	idy = np.arange(len(y))

	cm = plt.cm.get_cmap('OrRd') 
	mpl.rcParams['font.sans-serif'] = ['SimHei']
	mpl.rcParams['axes.unicode_minus'] = False
	
	im = imshow(sens_result, cmap=cm)
	plt.colorbar(im)
	plt.xticks(idx+width*2, x, rotation=30,fontsize=12)
	plt.yticks(idy+width*2, y, rotation=0,fontsize=18)
	for line in idx-0.5:
		plt.axvline(line, ls="-", color="black", alpha=0.3)
	for line in idy-0.5:
		plt.axhline(line, ls="-", color="black", alpha=0.3)
	plt.title(title+'敏感度分析', fontsize=35)
	plt.draw()
	# 导出与手动保存效果不一样，建议手动保存！
	# plt.savefig('敏感度分析-'+title+'.jpg', dpi=300, bbox_inches='tight')
	# plt.savefig('敏感度分析-'+title+'.jpg', dpi=300)
	plt.show()
	plt.close()