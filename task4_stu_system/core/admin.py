#_*_coding:utf-8*_
#Author:Fiona
import sys
from conf.settings import BASE_DIR
from .models import Teacher,School,Student,Study_score,Class,Class_course,Course,User
sys.path.append(BASE_DIR)
sys.path.append("..")

class Adminview(object):
    def __init__(self,session):
        self.session = session
        # self.run()
    # def run(self):
       #  menu = u'''
       # ------- 管理员主菜单 ---------
       #      \033[32;1m 1.  校区管理
       #      2.  讲师管理
       #      3.  创建用户
       #      b.  返回
       #      \033[0m'''
       #  exit_flag = False
       #  while not exit_flag:
       #      print(menu)
       #      option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
       #      if option == 'b':
       #          exit()
       #      elif option == '1':
       #          Adminview.school_manage(self)
       #      elif option == '2':
       #          Adminview.teacher_manage(self)
       #      elif option == '3':
       #          Adminview.user_manage(self)
       #      else:
       #          print("\033[31;1m菜单编号不存在，请重新输入\033[0m")
    def school_manage(self):
        exit_flag = False
        menu = u'''
        ------- 校区管理菜单 ---------\033[32;1m
                1.  创建校区
                b.  返回\033[0m
        '''
        while not exit_flag:
            print(menu)
            option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
            if option == 'b':
                exit_flag = True
            elif option == '1':
                school_name = input("\033[34;0m请输入创建校区的名称：\033[0m")
                addr = input("\033[34;0m请输入校区地址:\033[0m")
                school_obj = self.session.query(School).filter_by(school_name=school_name).first()
                if not school_obj:
                    school_new = School(school_name=school_name,address=addr)
                    self.session.add(school_new)
                    self.session.commit()
                    print("\033[34;1m学校创建成功\033[0m")
                anwser = input("\033[31;1m是否继续创建校区？（Y/N)：\033[0m").strip()
                if anwser == 'Y' or anwser == 'y':
                    continue
                elif anwser == 'N' or anwser == 'n':
                    exit_flag =True
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")
    def teacher_manage(self):
        exit_flag = False
        menu = u'''
        ------- 欢迎进入校区管理 ---------\033[32;1m
                1.  聘任讲师
                b.  返回\033[0m
        '''
        while not exit_flag:
            print(menu)
            option = input("请输入菜单编号：").strip()
            if option == 'b':
                exit_flag = True
            elif option == '1':
                teacher_name = input("\033[34;0m请输入聘任讲师的姓名：\033[0m")
                teacher_obj = self.session.query(Teacher).filter_by(teacher_name=teacher_name).first()
                if not teacher_obj:
                    teacher_new = Teacher(teacher_name=teacher_name)
                    self.session.add(teacher_new)
                    self.session.commit()
                anwser = input("\033[31;1m是否继续添加讲师？（Y/N)：\033[0m").strip()
                if anwser == 'Y' or anwser == 'y':
                    continue
                elif anwser == 'N' or anwser == 'n':
                    exit_flag =True
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")
    def user_manage(self):
        exit_flag = False
        print("当前用户列表：")
        for view_usertable in self.session.query(User.user_id.label('user_id'),User.username.label('name')).all():
            print(view_usertable.user_id,view_usertable.name)
        print("开始创建新用户账户----->")
        while not exit_flag:
            _username = input("请输入新用户名：").strip()
            _password = input("请输入新用户密码：").strip()
            _type = input("请输入新用户类型（admin/teacher/student）：").strip()
            if _type == "admin" or _type =="student" or _type =="teacher":
                user_obj = self.session.query(User).filter_by(username=_username).first()
                if not user_obj:
                    user_new = User(username=_username,password=_password,user_type=_type)
                    self.session.add(user_new)
                    self.session.commit()
                    print("\033[31;1m%s用户创建成功:\033[0m" % (_username))
                    exit_flag = True
            else:
                print("\033[31;1m用户类型输入错误，请重新输入！\033[0m")
                exit_flag = False