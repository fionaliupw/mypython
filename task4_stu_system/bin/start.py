#_*_coding:utf-8*_
#Author:Fiona

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

sys.path.append("..")

from core import main

if __name__ == '__main__':
    s = main.Action()
    s.login()
