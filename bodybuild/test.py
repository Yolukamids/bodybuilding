"""
-*- coding: utf-8 -*-
@Time : 2022/3/22 16:31
@Author : 风落心夜
@File : test
@Project : body
"""
import os
import re


imgs = os.listdir(r'D:\biyesheji\project\body\static\courses\img')
names = os.listdir(r'D:\biyesheji\project\body\static\courses\name')
lvls = os.listdir(r'D:\biyesheji\project\body\static\courses\lvl')
positions = os.listdir(r'D:\biyesheji\project\body\static\courses\position')
types = os.listdir(r'D:\biyesheji\project\body\static\courses\type')

rule = r'[0-9-]+(.*)'
for img, position, lvl, atype, name in zip(imgs, positions, lvls, types, names):
    img_g = 'courses/img/' + img
    name_g = re.findall(rule, name)[0][:-4]
    atype_g = re.findall(rule, atype)[0][:-4]
    lvl_g = re.findall(rule, lvl)[0][:-4]
    position_g = re.findall(rule, position)[0][:-4]
    print(img_g, name_g, atype_g, lvl_g, position_g)
