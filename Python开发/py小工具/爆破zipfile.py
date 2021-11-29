#!/usr/bin/python3
# -*- coding: utf-8 -*-


import zipfile
from threading import Thread
file = zipfile.ZipFile("test.zip", 'r')


def Dictionaries():
    pass


def Runzip(Dicts):
    for password in range(0, 999999):
        try:
            file.extractall(pwd=str(password).encode())
            print('破解成功，密码：{}'.format(password))
            file.close()
            break
        except Exception:
            pass

Thread(target=Runzip(1)).start()