# -*- coding:utf-8 -*-
import turtle
import time


# 画心形圆弧


def hart_arc():
    for i in range(200):
        turtle.right(1)
        turtle.forward(2)


def move_pen_position(x, y):
    turtle.hideturtle()  # 隐藏画笔（先）

    turtle.up()  # 提笔

    turtle.goto(x, y)  # 移动画笔到指定起始坐标（窗口中心为0,0）

    turtle.down()  # 下笔

    turtle.showturtle()  # 显示画笔

    # 初始化

    turtle.setup(width=800, height=500)  # 窗口（画布）大小

    turtle.color('red', 'pink')  # 画笔颜色

    turtle.pensize(2)  # 画笔粗细

    turtle.speed(0.5)  # 描绘速度

    # 初始化画笔起始坐标

    move_pen_position(x=0, y=-180)  # 移动画笔位置

    turtle.left(140)  # 向左旋转140度

    turtle.begin_fill()  # 标记背景填充位置

    # 画心形直线（ 左下方 ）

    turtle.forward(224)  # 向前移动画笔，长度为224

    # 画爱心圆弧

    hart_arc()  # 左侧圆弧

    turtle.left(120)  # 调整画笔角度

    hart_arc()  # 右侧圆弧

    # 画心形直线（ 右下方 ）

    turtle.forward(224)

    turtle.end_fill()  # 标记背景填充结束位置

    # 点击窗口关闭程序

    window = turtle.Screen()

    window.exitonclick()
