#_*_coding:utf-8*_
#Author:Fiona

import sys
from conf.settings import BASE_DIR
from .models import Teacher,School,Student,Study_score,Class,Class_course,Course,User
sys.path.append(BASE_DIR)
sys.path.append("..")

class Studentview(object):
    def __init__(self,session):
        self.session = session

    def add_tuition(self,stu_obj):
        exit_flag = False
        while not exit_flag:
            student_name = input("\033[34;0m请输入学生的姓名：\033[0m")
            class_name = input("\033[34;0m请输入所注册的班级名：\033[0m")
            class_obj = self.session.query(Class).filter_by(class_name=class_name).first()
            if class_obj and class_obj.students[0] == stu_obj:
                tuition1 = input("\033[34;0m请输入%s学员需缴纳的学费:\033[0m" % stu_obj.student_name).strip()
                tuition = float(tuition1)
                stu_new = Student(student_name=student_name,tuition=tuition)
                self.session.add(stu_new)
                self.session.commit()
                print("\033[34;1m学员交费成功！\033[0m")
            else:
                print("\33[31;1m班级不存在或没有权限管理此班级\33[0m")

