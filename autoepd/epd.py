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
import seaborn as sns
from pylab import *
# plt.style.use('seaborn') #使用seaborn画图风格

# main--------------------------------------------------------------------------------------
def main(file_input, file_result, product_num, product_name, unit_field):
	workbook = xlrd.open_workbook(file_input)
	table_head_stage = lf.get_table_head(file_input, 0)
	table_head_chara = lf.get_table_head(file_input, 1)
	stage_row, stage_numlist = lf.get_Head_numlist(table_head_stage)
	chara_row, chara_numlist = lf.get_Head_numlist(table_head_chara)
	list_stage_head, list_stage_head_lable, list_chara_head, list_chara_head_lable = lf.get_list_head(table_head_stage, table_head_chara, stage_row, stage_numlist, chara_row, chara_numlist)
	table_res_lable = lf.get_table_res_lable(file_input, list_stage_head_lable)
	table_chara_lable = lf.get_table_chara_lable(file_input, list_chara_head_lable)

	table_mul, table_total, table_result = lf.get_epd(product_num, table_head_stage, table_head_chara, list_stage_head_lable, list_chara_head, list_chara_head_lable, table_res_lable, table_chara_lable)

	# 导出excel----------------------------------------------------
	writer = pd.ExcelWriter(file_result)
	for ind, tab in enumerate(table_result):
		tab.to_excel(writer,product_name[ind])
	writer.save()
	lf.get_csv(file_input, file_result, unit_field)

	return table_mul, table_total, table_result

# # 调试时，如果要查看每个变量，在spyder中运行以下代码，实质为上述main()--------------------------------------------------
# file_input = 'input_陶瓷砖_东鹏.xlsx'
# file_result = 'result.xlsx'
# product_num = 5
# product_name = ['600×600抛光砖', '800×800抛光砖', '800×800干法原石', '800×800湿法原石', '900x900干法原石']

# workbook = xlrd.open_workbook(file_input)
# table_head_stage = lf.get_table_head(file_input, 0)
# table_head_chara = lf.get_table_head(file_input, 1)
# stage_row, stage_numlist = lf.get_Head_numlist(table_head_stage)
# chara_row, chara_numlist = lf.get_Head_numlist(table_head_chara)
# list_stage_head, list_stage_head_lable, list_chara_head, list_chara_head_lable = lf.get_list_head(table_head_stage, table_head_chara, stage_row, stage_numlist, chara_row, chara_numlist)
# table_res_lable = lf.get_table_res_lable(file_input, list_stage_head_lable)
# table_chara_lable = lf.get_table_chara_lable(file_input, list_chara_head_lable)

# table_mul, table_total, table_result = lf.get_epd(product_num, table_head_stage, table_head_chara, list_stage_head_lable, list_chara_head, list_chara_head_lable, table_res_lable, table_chara_lable)
# # 导出excel----------------------------------------------------
# 	writer = pd.ExcelWriter(file_result)
# 	for ind, tab in enumerate(table_result):
# 		tab.to_excel(writer,product_name[ind])
# 	writer.save()

# 	lf.get_csv(file_input, file_result)

















# # plot----------------------------------------------------------
# # cm = plt.get_cmap('Oranges')
# # x = np.random.rand(30)
# # y = np.random.rand(30)
# # z = np.random.rand(30)
# # col = [cm(float(i)/(30)) for i in range(30)]

# # zhfont1 = matplotlib.font_manager.FontProperties(fname='/home/gift/.fonts/yaheiMonaco.ttf') # for Ubuntu

# mpl.rcParams['font.sans-serif'] = ['SimHei']
# mpl.rcParams['axes.unicode_minus'] = False
# # table_result_m2_1.ix[0,range(0,stage_row)].plot(kind='bar',stacked=False,alpha=0.7)
# table_result.ix[0,range(0,stage_row)].plot(kind='bar',stacked=False,alpha=0.7)
# # plt.xlabel(u"横坐标",fontproperties=zhfont1)
# # plt.title(u'全球变暖',fontsize=18,fontproperties=zhfont1)
# plt.title(u'全球变暖',fontsize=18)
# plt.ylabel(u'kg CO2 eq')

# # x = table_result_m2_1.columns
# x = table_result.columns
# width = 0.0
# idx = np.arange(len(x))

# # plt.xticks(idx+width*2, x, rotation=0,fontsize=18,fontproperties=zhfont1)
# plt.xticks(idx+width*2, x, rotation=0,fontsize=18)



# # plt.legend()

# plt.xlim(-0.5,4.5)
# # plt.ylim(0,15)

# plt.savefig('全球变暖.jpg',dpi=300)
# plt.show()


# # table_result.iloc[1].sort_values(inplace=False, ascending=True)
# # table_result.iloc[1] = table_result.iloc[1].sort_values(inplace=False, ascending=True)
# # plt.xticks(idx+width*2, x, rotation=0,fontsize=18)

# # myfont = FontProperties(fname='/home/gift/.fonts/timesi.ttf')  

# # plt.barh(range(len(table_result.iloc[1])), table_result.iloc[1], alpha=0.7, color=col)
# # print (table_result.sum(axis=1))


