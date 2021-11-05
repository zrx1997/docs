#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project： sd_wan_client
# @Time: 2021/9/30 14:30
# @Author： kf
# @File： 国旗渐变
# @Software： PyCharm

from PIL import Image

if __name__ == '__main__':
    # 读取图片
    guoqi = Image.open('五星红旗.png')
    touxiang = Image.open('头像.jpg')

    # 获取国旗的尺寸
    x, y = guoqi.size
    # 根据需求，设置左上角坐标和右下角坐标（截取的是正方形）
    quyu = guoqi.crop((262, 100, y + 62, y - 100))

    # 获取头像的尺寸
    w, h = touxiang.size
    # 将区域尺寸重置为头像的尺寸
    quyu = quyu.resize((w, h))
    # 透明渐变设置
    for i in range(w):
        for j in range(h):
            color = quyu.getpixel((i, j))
            alpha = 255 - i // 3
            if alpha < 0:
                alpha = 0
            color = color[:-1] + (alpha,)
            quyu.putpixel((i, j), color)

    # 粘贴到头像并保存
    touxiang.paste(quyu, (0, 0), quyu)
    touxiang.save('五星红旗半透明渐变头像.png')


