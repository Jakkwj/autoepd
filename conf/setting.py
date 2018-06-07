#!/usr/bin/env python  
# -*- coding: utf-8 -*-
# Author: JunWang

import os  
import sys  
  
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   #根目录  
FUNCTIONS_DIR = BASE_DIR+"\lib"  #自定义模块目录
print(BASE_DIR)  
print(os.path.dirname(os.path.abspath(__file__)))      #返回不带文件名的目录名  
print(os.path.abspath(__file__))   #返回当前程序的绝对路径\  
print(__file__)       #返回当前程序的相对路径/  

#添加环境变量  
sys.path.append(BASE_DIR) 
sys.path.append(FUNCTIONS_DIR) 

# from conf import settings  
# from core import main  
  
# main.login()  