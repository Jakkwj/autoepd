# -*- coding: utf-8 -*-

import pandas as pd  
import collections
import csv
import psycopg2
import xlrd

# -----------------------------------------------------------------------------------------

def csv_export(csvfile_name, fieldnames, data):
	with open(csvfile_name, 'w', newline='') as csvfile: #Ubuntu
	# with open(csvfile_name, 'w', encoding='UTF8', newline='') as csvfile: #windows
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(data)

def get_csv(filename):
	get_dict = collections.defaultdict()
	get_list = []
	workbook = xlrd.open_workbook(filename)
	for sheet in workbook.sheet_names():
		data_xls = pd.read_excel('%s'%(file), sheet, index_col = 0)
		for col in data_xls:
			counter = 0
			for data in data_xls[col]:
				get_dict = {'product': sheet, 'stage': col, 'chara': data_xls.index[counter],  'unit':unit_field['%s'%(data_xls.index[counter])] , 'result': data}
				get_list.append(get_dict)
				counter += 1
	csv_export("result.csv",field, get_list)

def creat_table():
	conn = psycopg2.connect(database="EPD", user="postgres", password="gift", host="127.0.0.1", port="5432")
	cur = conn.cursor()
	cur.execute('''CREATE TABLE Results(
		product	TEXT,
		stage	TEXT,
		chara	TEXT,
		result	REAL,
		unit	TEXT,
		PRIMARY KEY (product, stage, chara)
			)''')
	
	conn.commit()
	cur.close()
	conn.close()  


def import_csv():
	conn = psycopg2.connect(database="EPD", user="postgres", password="gift", host="127.0.0.1", port="5432")
	cur = conn.cursor()

	cur.execute("COPY Results from '/home/gift/Public/Data/gift/Cloud/CloudStation/标准化院/项目/EPD/Py/result.csv' with csv header")
	# cur.execute("COPY Results from 'E:/CloudStation/标准化院/项目/EPD/Py/result.csv' with csv header")

	conn.commit()
	cur.close()
	conn.close()

def drop_table():
	conn = psycopg2.connect(database="EPD", user="postgres", password="gift", host="127.0.0.1", port="5432")
	cur = conn.cursor()
	cur.execute('''DROP TABLE Results''')
	conn.commit()
	cur.close()
	conn.close()




def main():
	# get_csv(file)
	# creat_table()
	import_csv()
	# drop_table()
	# select()
	# pass
# -----------------------------------------------------------------------------------------

file = 'result.xlsx'
field = ['product', 'stage', 'chara', 'result', 'unit']
unit_field = {'全球变暖':'kg CO2 eq', '光化学烟雾':'kg C2H4 eq', '酸化效应':'kg SO2 eq', '富营养化':'kg PO43- eq', '不可再生资源消耗':'kg antimony eq', '中国化石能源消耗':'kg coal eq'}
# -----------------------------------------------------------------------------------------

if __name__ == "__main__":
	main()





	