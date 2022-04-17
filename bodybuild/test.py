"""
-*- coding: utf-8 -*-
@Time : 2022/3/22 16:31
@Author : 风落心夜
@File : test
@Project : body
"""
import os
import re


names = os.listdir('D:/biyesheji/project/body/static/images/actions')
print(names)
pic_url = os.listdir('D:/biyesheji/project/body/static/images/actions')
postions = os.listdir('D:/biyesheji/project/body/static/position')
lvls = os.listdir('D:/biyesheji/project/body/static/lvl')
types = os.listdir('D:/biyesheji/project/body/static/type')
videos = os.listdir(r'D:\biyesheji\project\body\static\video')

rule = r'[0-9-]+[0-9]+(.*)'
i = 1
for url, position, lvl, atype, name, video in zip(pic_url, postions, lvls, types, names, videos):
    url_g = 'images/actions/' + url
    video_g = 'video/' + video
    name_g = re.findall(rule, name)[0][:-4]
    atype_g = re.findall(rule, atype)[0][:-4]
    lvl_g = re.findall(rule, lvl)[0][:-4]
    position_g = re.findall(rule, position)[0][:-4]
    print(url_g, video_g, name_g, position_g, lvl_g, atype_g)
