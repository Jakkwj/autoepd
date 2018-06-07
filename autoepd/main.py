# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import epd, sens

# input变量----------------------------------------------------------------------
# file_input = 'input_JZT-C1T06_sens.xlsx'
# product_num = 1
# product_name = ['JZT-C1T06']

file_input = 'input_陶瓷砖_东鹏.xlsx'
product_num = 5
product_name = ['600×600抛光砖', '800×800抛光砖', '800×800干法原石', '800×800湿法原石', '900x900干法原石']

unit_field = {'全球变暖':'kg CO2 eq', '光化学烟雾':'kg C2H4 eq', '酸化效应':'kg SO2 eq', '富营养化':'kg PO43- eq', '不可再生资源消耗':'kg antimony eq', '中国化石能源消耗':'kg coal eq'}
file_result = 'result.xlsx'
delta_x = 0.1 # x增加为原来的10%，即1.1倍

# main--------------------------------------------------------------------------------------
table_mul, table_total, table_result = epd.main(file_input, file_result, product_num, product_name, unit_field)
# sens.main(file_input, product_num, product_name, delta_x)