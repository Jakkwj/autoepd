# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import epd

epd = epd.epd()
epd.file_input = 'input_epd_exam.xlsx'
epd.file_result = 'result.xlsx'
epd.file_result_csv = "result.csv"
epd.product_num = 5
epd.product_name = ['Product1', 'Product2', 'Product3', 'Product4', 'Product5']
epd.unit_field = {'全球变暖':'kg CO2 eq', '光化学烟雾':'kg C2H4 eq', '酸化效应':'kg SO2 eq', '富营养化':'kg PO43- eq', '不可再生资源消耗':'kg antimony eq', '中国化石能源消耗':'kg coal eq'}
epd.delta_x = 0.1 # x增加为原来的10%，即1.1倍

epd.initialise()
epd.get_epd(epd.product_num, epd.table_res_lable) # get EPD results
epd.epd_resultsave() # get results xlsx and csv format
epd.get_sensitivity() # sensitivity results
