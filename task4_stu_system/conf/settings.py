#_*_coding:utf-8*_
#Author:Fiona
import os,sys
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

engine = create_engine("mysql+pymysql://stu:Qwer0987!@localhost:3306/pythondb",encoding="utf-8",echo=True)