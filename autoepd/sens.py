# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import lib.functions as lf
from matplotlib.font_manager import *  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import xlwt
import csv
import os
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import seaborn as sns
from pylab import *
import copy
# plt.style.use('seaborn') #使用seaborn画图风格

# main--------------------------------------------------------------------------------------
def main(file_input, product_num, product_name, delta_x):
	workbook = xlrd.open_workbook(file_input)
	table_head_stage = lf.get_table_head(file_input, 0)
	table_head_chara = lf.get_table_head(file_input, 1)
	stage_row, stage_numlist = lf.get_Head_numlist(table_head_stage)
	chara_row, chara_numlist = lf.get_Head_numlist(table_head_chara)
	list_stage_head, list_stage_head_lable, list_chara_head, list_chara_head_lable = lf.get_list_head(table_head_stage, table_head_chara, stage_row, stage_numlist, chara_row, chara_numlist)
	table_res_lable = lf.get_table_res_lable(file_input, list_stage_head_lable)
	table_chara_lable = lf.get_table_chara_lable(file_input, list_chara_head_lable)
	sens_table_res_lable = lf.get_sens_table_res_lable(file_input, list_stage_head_lable, table_res_lable, product_num, delta_x)

	#构建一个最后一行为企业数据input的df，即product_num=1时的table_res_lable----------------
	trl_copy = copy.deepcopy(table_res_lable)
	trl_copy.drop(trl_copy.index[range(-1,-product_num,-1)],inplace=True)
	trl_copy_copy = copy.deepcopy(table_res_lable)
	sen_product_num = 1 #每次只计算一个产品

	# #依次对每一个产品求sens-----------------------------
	for num in range(product_num):
		trl_copy.iloc[-1] = trl_copy_copy.iloc[-(product_num-num)]
		sens_table_res_lable = lf.get_sens_table_res_lable(file_input, list_stage_head_lable, trl_copy, product_num, delta_x)

		# 求sens列表，sens为灵敏度计算结果矩阵-----------------------------
		table_mul, table_total, table_result = lf.get_epd(sen_product_num, table_head_stage, table_head_chara, list_stage_head_lable, list_chara_head, list_chara_head_lable, trl_copy, table_chara_lable)
		sens_raw = copy.deepcopy(table_result)
		sens = []
		for tab in sens_table_res_lable:
			table_mul, table_total, table_result = lf.get_epd(sen_product_num, table_head_stage, table_head_chara, list_stage_head_lable, list_chara_head, list_chara_head_lable, tab, table_chara_lable)
			sens.append(lf.senstivity(sens_raw[0], table_result[0], delta_x))

		# sens_result按阶段解析结果-------------------------------------
		sens_result=[]
		sen_plot = pd.DataFrame()
		for row in range(stage_row):
			# sen_plot = pd.DataFrame()
			for idx in range(stage_numlist[row],stage_numlist[row+1]):
				sens_result.append(sens[idx][table_head_stage.columns[stage_numlist[row]]])
			# for idx, lsh in enumerate(list_stage_head[row]):
			for idx, lsh in enumerate(list_stage_head_lable[row]):
				sen_plot[lsh] = sens_result[idx]
			# lf.sens_plot(sen_plot,table_head_stage.columns[stage_numlist[row]])
		lf.sens_plot(sen_plot,product_name[num])







# # 调试时，如果要查看每个变量，在spyder中运行以下代码，实质为上述main()--------------------------------------------------
# # file_input = 'input_JZT-C1T06_sens.xlsx'
# # product_num = 1
# # delta_x = 0.1 # x增加为原来的10%，即.1倍
# # product_name = ['JZT-C1T06']

# file_input = 'input_陶瓷砖_东鹏.xlsx'
# product_num = 5
# delta_x = 0.1 # x增加为原来的10%，即.1倍
# product_name = ['600×600抛光砖', '800×800抛光砖', '800×800干法原石', '800×800湿法原石', '900x900干法原石']

# workbook = xlrd.open_workbook(file_input)
# table_head_stage = lf.get_table_head(file_input, 0)
# table_head_chara = lf.get_table_head(file_input, 1)
# stage_row, stage_numlist = lf.get_Head_numlist(table_head_stage)
# chara_row, chara_numlist = lf.get_Head_numlist(table_head_chara)
# list_stage_head, list_stage_head_lable, list_chara_head, list_chara_head_lable = lf.get_list_head(table_head_stage, table_head_chara, stage_row, stage_numlist, chara_row, chara_numlist)
# table_res_lable = lf.get_table_res_lable(file_input, list_stage_head_lable)
# table_chara_lable = lf.get_table_chara_lable(file_input, list_chara_head_lable)

# #构建一个最后一行为企业数据input的df，即product_num=1时的table_res_lable----------------
# trl_copy = copy.deepcopy(table_res_lable)
# trl_copy.drop(trl_copy.index[range(-1,-product_num,-1)],inplace=True)
# trl_copy_copy = copy.deepcopy(table_res_lable)
# sen_product_num = 1 #每次只计算一个产品

# # #依次对每一个产品求sens-----------------------------
# for num in range(product_num):
# 	trl_copy.iloc[-1] = trl_copy_copy.iloc[-(product_num-num)]
# 	print(-(product_num-num))
# 	sens_table_res_lable = lf.get_sens_table_res_lable(file_input, list_stage_head_lable, trl_copy, product_num, delta_x)

# 	# 求sens列表，sens为灵敏度计算结果矩阵-----------------------------
# 	for tab in sens_table_res_lable:
# 		table_mul, table_total, table_result = lf.get_epd(sen_product_num, table_head_stage, table_head_chara, list_stage_head_lable, list_chara_head, list_chara_head_lable, tab, table_chara_lable)
# 		sens.append(lf.senstivity(sens_raw[0], table_result[0], delta_x))

# 	# sens_result按阶段解析结果-------------------------------------
# 	sens_result=[]
# 	sen_plot = pd.DataFrame()
# 	for row in range(stage_row):
# 		# sen_plot = pd.DataFrame()
# 		for idx in range(stage_numlist[row],stage_numlist[row+1]):
# 			sens_result.append(sens[idx][table_head_stage.columns[stage_numlist[row]]])
# 		# for idx, lsh in enumerate(list_stage_head[row]):
# 		for idx, lsh in enumerate(list_stage_head_lable[row]):
# 			sen_plot[lsh] = sens_result[idx]
# 		# lf.sens_plot(sen_plot,table_head_stage.columns[stage_numlist[row]])
# 	lf.sens_plot(sen_plot,product_name[num])