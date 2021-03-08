#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
print("请输入要查找的路径，分隔符要用双斜杠：(c:\\d\\e)")
path = input(">>>")   # 要遍历的目录
print("请输入要查找的后缀，如.mp4, .txt等")
suffix = input(">>>")
lst = []
for root, dirs, names in os.walk(path):
    for name in names:
        ext = os.path.splitext(name)[1]  # 获取后缀名
        if ext == suffix:
            fromdir = os.path.join(root, name)  # mp4文件原始地址
            lst.append(fromdir)
            os.remove(fromdir)  # 删除文件
            print("文件{%s}删除成功~" % fromdir)

#
# with open("rmdir_file.txt", mode="wt",encoding="utf-8") as f:
#     json.dump(lst,f)
