
#引入turtle函数库

from turtle import *

#定义画半个太极图的函数，第一个参数radius是大圆的半径，

#color1，color2分别是两种填充颜色，对应图形中的黑白填充

def draw(radius, color1,color2):

    #设置画笔粗细
    width(3)

    #设置画笔颜色和填充颜色
    color("black",color1)

    #准备开始填充图形
    begin_fill()

    #首先画一个半径为radius/2，弧度为180的半圆，画的是红线所示半圆
    circle(radius/2,180)

    #画一个半径为radius，弧度为180的半圆，画的是黄线所示半圆
    circle(radius,180)

    #将画笔方向旋转180度
    left(180)

    #画一个半径为radius/2，弧度为180的半圆，此时半径值为负，

    #圆心在画笔的右边，画的是绿线所示半圆
    circle(-radius/2,180)

    #结束填充
    end_fill()

    #画笔向左旋转90度，正好指向画板上方

    left(90)

    #抬起画笔，再运动时不会留下痕迹
    up()

    #向前移动radius*0.35，这样小圆边线距离大圆边线上下各radius*0.35，

    #圆的半径就为radius*0.15
    forward(radius*0.35)

    #画笔向右旋转90度，指向画板右侧
    right(90)

    #放下画笔
    down()

    color(color2,color2)

    #开始画内嵌小圆，如蓝线所示
    begin_fill()

    circle(radius*0.15)

    end_fill()

    #旋转画笔90度，指向画板上方
    left(90)

    up()

    #后退radius*0.35
    backward(radius*0.35)

    down()

    #旋转画笔90度，指向画板左方
    left(90)

#定义主函数
def main():

    #设置窗口或者画板大小
    setup(500,500)

    #绘制黑色一半，白色内圆
    draw(200,"black","white")

    #绘制白色一半，黑色内圆
    draw(200,"white","black")

    #隐藏画笔
    ht()

main()
