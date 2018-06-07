#_*_coding:utf-8*_
#Author:Fiona

import sys
from conf.settings import BASE_DIR,engine
from sqlalchemy.orm import sessionmaker
from .models import Teacher,School,Student,Study_score,Class,Class_course,Course,User
from .admin import Adminview
from .teacher import Teacherview
from .student import Studentview

sys.path.append(BASE_DIR)
sys.path.append("..")

class Action(object):
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.login()

    def login(self):
        print("欢迎进入学生管理系统".center(50,'-'))
        _username_ = input("请输入用户名：").strip()
        _password_ = input("请输入密码：").strip()
        self.user_obj = self.session.query(User).filter(User.username==_username_,User.password==_password_).first()
        if self.user_obj:
            print("\033[36;1m【%s】登录成功\033[0m" % self.user_obj.username)
            if self.user_obj.user_type == 'admin':
                admin = Adminview(self.session)
                menu = u'''
               ------- 管理员主菜单 ---------
                    \033[32;1m 1.  校区管理
                    2.  讲师管理
                    3.  创建用户
                    b.  返回
                    \033[0m'''
                exit_flag = False
                while not exit_flag:
                    print(menu)
                    option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
                    if option == 'b':
                        exit()
                    elif option == '1':
                        admin.school_manage()
                    elif option == '2':
                        admin.teacher_manage()
                    elif option == '3':
                        admin.user_manage()
                    else:
                        print("\033[31;1m菜单编号不存在，请重新输入\033[0m")
            elif self.user_obj.user_type == 'teacher':
                teacher=Teacherview(self.session)
                menu = u'''
               ------- 讲师主菜单 ---------
                    \033[32;1m 1.  添加班级
                    2.  添加课程
                    3.  注册学员
                    4.  添加成绩
                    5.  修改成绩
                    b.  返回
                    \033[0m'''
                teacher_name = input("\033[34;0m请输入班级讲师的姓名：\033[0m")
                self.teacher_obj = self.session.query(Teacher).filter_by(teacher_name=teacher_name).first()
                exit_flag = False
                while not exit_flag:
                    print(menu)
                    option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
                    if option == 'b':
                        exit()
                    elif option == '1':
                        teacher.class_manage(self.teacher_obj)
                    elif option == '2':
                        teacher.course_manage(self.teacher_obj)
                    elif option == '3':
                        teacher.add_student(self.teacher_obj)
                    elif option == '4':
                        teacher.add_score(self.teacher_obj)
                    elif option == '5':
                        teacher.modify_score(self.teacher_obj)
                    else:
                        print("\033[31;1m菜单编号不存在，请重新输入\033[0m")
            elif self.user_obj.user_type == 'student':
                student=Studentview(self.session)
                menu = u'''
               ------- 学生主菜单 ---------
                    \033[32;1m 1.  交费
                    b.  返回
                    \033[0m'''
                student_name = input("\033[34;0m请输入学员的姓名：\033[0m")
                self.stu_obj = self.session.query(Student).filter_by(student_name=student_name).first()
                exit_flag = False
                while not exit_flag:
                    print(menu)
                    option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
                    if option == 'b':
                        exit()
                    elif option == '1':
                        student.add_tuition(self.stu_obj)
                    else:
                        print("\033[31;1m菜单编号不存在，请重新输入\033[0m")
        else:
            print("用户名或密码输入错误！")