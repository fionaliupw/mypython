#_*_coding:utf-8*_
#Author:Fiona

import os,sys,json
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append("..")

# 文件路径
data_dir = os.path.join(os.path.sep,BASE_DIR,'data')
data_admin = os.path.join(os.path.sep,data_dir,'admin')
data_school = os.path.join(os.path.sep,data_dir,'school')
data_course = os.path.join(os.path.sep,data_dir,'course')
data_student = os.path.join(os.path.sep,data_dir,'student')
data_teacher = os.path.join(os.path.sep,data_dir,'teacher')
user_file = os.path.join(os.path.sep,BASE_DIR,data_admin,'user.json')

class operation(object):
    def __init__(self):
        pass
    def save(self,type,list,dict):
        filename = type+r'_save.pk'
        dict['file'] = filename
        filepath = "%s\%s"%(data_dir,type)
        save_file = "%s\%s"%(filepath,filename)
        if os.path.isdir(filepath):
            with open(save_file,"wb") as f:
                pickle.dump(list,f)
            print("--------",type,"创建成功","--------")
            for item in list:
                print(item)
        return True
    def save_list(self,type,list):
        filename = type+r'_save.pk'
        filepath = "%s\%s"%(data_dir,type)
        save_file = "%s\%s"%(filepath,filename)
        if os.path.isdir(filepath):
            with open(save_file,"wb") as f:
                f.write(pickle.dumps(list))
                print("--------",type,"创建成功","--------")
                for i in list:
                    for key in i:
                        print(key,i[key])
                    print("\n")
        return True
    def open(self,type):
        all_data = []
        filename = type+r'_save.pk'
        filepath = "%s\%s"%(data_dir,type)
        open_file = "%s\%s"%(filepath,filename)
        if os.path.exists(open_file):
            with open(open_file,"rb") as f:
                all_data = pickle.load(f)
            # print(all_data)
        else:
            new = open(open_file,"w")
            new.close()
        return all_data

# 管理员类
class admin(operation):
    def __init__(self):
        operation.__init__(self)
    def create_user(self):
        with open(user_file,"r") as f:
            user = json.load(f)
        print("当前用户列表：")
        for key,value in user.items():
            print("%s:%s" % (key,value))
        print("开始创建新用户账户----->")
        _username_ = input("请输入新用户名：").strip()
        _password_ = input("请输入新用户密码：").strip()
        exit_flag = False
        while not exit_flag:
            _type_ = input("请输入新用户类型（admin/teacher/student）：").strip()
            if _type_ == "admin" or _type_ == "teacher" or _type_ == "student":
                dict_temp = {}
                dict_temp["password"] = _password_
                dict_temp["type"] = _type_
                user[_username_] = dict_temp
                print("\033[31;1m%s用户创建成功:\033[0m" % (_username_))
                print("%s:%s" % (_username_,dict_temp))
                with open(user_file,"w") as fw:
                    json.dump(user,fw)
                exit_flag = True
            else:
                print("\033[31;1m用户类型输入错误，请重新输入！\033[0m")
                exit_flag = False
    def create_school(self):
        school_data = operation.open(self,"school")
        school_dict = {}
        school_name = input("输入所创建的学校名称：").strip()
        school_addr = input("输入学校地址：").strip()
        school_leader = input("输入学校负责人：").strip()
        school_phone = input("输入学校电话：").strip()
        sl = school(school_name,school_addr,school_leader,school_phone)
        school_dict["学校名称"] = sl.school_name
        school_dict["学校地址"] = sl.school_addr
        school_dict["负责人"] = sl.school_leader
        school_dict["电话"] = sl.school_phone
        school_data.append(school_dict)
        operation.save(self,"school",school_data,school_dict)
    def create_course(self):
        course_data = operation.open(self,"course")
        course_dict = {}
        course_name = input("输入所创建的课程名：").strip()
        course_school = input("输入开设此课程的学校名称：").strip()
        course_price = input("输入课程价格：").strip()
        course_teacher = input("输入带课老师：").strip()
        cs = course(course_name,course_school,course_price,course_teacher)
        course_dict["课程名"] = cs.course_name
        course_dict["开设学校"] = cs.course_school
        course_dict["课程价格"] = cs.course_price
        course_dict["带课老师"] = cs.course_teacher
        course_data.append(course_dict)
        operation.save(self,"course",course_data,course_dict)
    def invite_teacher(self):
        teacher_data = operation.open(self,"teacher")
        teacher_dict = {}
        teacher_name = input("请输入讲师姓名：").strip()
        teacher_salary = input("请输入讲师薪资：").strip()
        teacher_school = input("请输入任教学校：").strip()
        teacher_course = input("请输入带教课程：").strip()
        tr = teacher(teacher_name,teacher_salary,teacher_school,teacher_course)
        teacher_dict["讲师姓名"] = tr.teacher_name
        teacher_dict["讲师薪资"] = tr.teacher_salary
        teacher_dict["任教学校"] = tr.teacher_school
        teacher_dict["带教课程"] = tr.teacher_course
        teacher_data.append(teacher_dict)
        operation.save(self,"teacher",teacher_data,teacher_dict)

# 学校类
class school(operation):
    def __init__(self,school_name,school_addr,school_leader,school_phone):
        operation.__init__(self)
        self.school_name = school_name
        self.school_addr = school_addr
        self.school_leader = school_leader
        self.school_phone = school_phone

# 课程类
class course(operation):
    def __init__(self,course_name,course_school,course_price,course_teacher):
        operation.__init__(self)
        self.course_name = course_name
        self.course_school = course_school
        self.course_price = course_price
        self.course_teacher = course_teacher


# 讲师类
class teacher(operation):
    def __init__(self,teacher_name,teacher_salary,teacher_school,teacher_course):
        operation.__init__(self)
        self.teacher_name = teacher_name
        self.teacher_salary = teacher_salary
        self.teacher_school = teacher_school
        self.teacher_course = teacher_course
    def print_student(self):
        all_student = operation.open(self,"student")
        # print(all_student)
        # 通过学校和讲师授课课程统计该课程下的学生人数count
        t_course = input("请输入课程：").strip()
        t_school = input("请输入学校：").strip()
        count = 0
        print_data = []
        for item in all_student:
            if item["课程"] == t_course and item["学校"]== t_school:
                count += 1
                print_data.append(item["学生姓名"])
            else:
                count += 0
        print("\033[31;1m%s\033[0m学校的\033[31;1m%s\033[0m课程共有\033[31;1m%s\033[0m个学员" % (t_school,t_course,count))
        print("\033[31;1m学员列表如下：\033[0m")
        if count == 0:
            print("\033[31;1m该课程暂时没有学员注册。\033[0m")
        else:
            for index,i in enumerate(print_data):
                print("|  序号  |  学生姓名  |")
                print("    %s        %s     " % (index,i))
    def register_score(self):
        student_score = []
        student_school = input("请输入学校：").strip()
        student_course = input("请输入课程：").strip()
        student_list = operation.open(self,"student")
        for item in student_list:
            if item["课程"] == student_course and item["学校"]== student_school:
                student_name = item["学生姓名"]
                score = input("请输入%s 的成绩：" % student_name).strip()
                item["成绩"] = score
                item.pop("file")
                student_score.append(item)
            else:
                print("学校与课程信息输入不匹配！")
        operation.save_list(self,"score",student_score)
    def update_score(self):
        student_school = input("请输入学校：").strip()
        student_course = input("请输入课程：").strip()
        student_name = input("请输入学生姓名：").strip()
        student_score = operation.open(self,"score")
        for item in student_score:
            if item["课程"] == student_course and item["学校"]== student_school and item["学生姓名"] == student_name:
                tips = "|  学生姓名   |   学校   |   课程   |   成绩   |"
                print(tips)
                print("|   %s   |   %s   |   %s   |   %s   |" % (student_name,student_school,student_course,item["成绩"]))
                update_flag = False
                update_ask = input("是否修改成绩？（Y/N)").strip()
                if update_ask == 'Y' or update_ask == 'y':
                    update_flag = True
                elif update_ask == 'N' or update_ask == 'n':
                    update_flag =True
                if update_flag:
                    score = input("请输入%s的最新成绩：" % student_name).strip()
                    item["成绩"] = score
            else:
                print("不存在该名学生！")
            operation.save_list(self,"score",student_score)

    def view_score(self):
        student_score = operation.open(self,"score")
        for item in student_score:
            print(item)
# 学生类
class student(operation):
    def __init__(self,student_name,student_sex,student_school,student_course,student_tution):
        operation.__init__(self)
        self.student_name = student_name
        self.student_sex = student_sex
        self.student_school = student_school
        self.student_course = student_course
        self.student_tution = student_tution
    def student_register(self):
        student_data = operation.open(self,"student")
        student_dict = {}
        student_name = input("输入学生姓名：").strip()
        student_sex = input("输入性别(Female or Male)：").strip()
        student_school = input("输入注册学校：").strip()
        student_course = input("输入注册课程:").strip()
        student_tution = input("缴纳学费:").strip()
        stu = student(student_name,student_sex,student_school,student_course,student_tution)
        student_dict["学生姓名"] = stu.student_name
        student_dict["性别"] = stu.student_sex
        student_dict["学校"] = stu.student_school
        student_dict["课程"] = stu.student_course
        student_dict["学费"] = stu.student_tution
        student_data.append(student_dict)
        operation.save(self,"student",student_data,student_dict)

# 管理员视图
class adminview(admin):
    def __init__(self):
        admin.__init__(self)
    def login(self):
        menu = u'''
       ------- 管理员主菜单 ---------
            \033[32;1m 1.  校区管理
            2.  讲师管理
            3.  课程管理
            4.  创建用户
            5.  返回
            \033[0m'''
        menu_dict = {
            '1':adminview.school_manage,
            '2':adminview.teacher_manage,
            '3':adminview.course_manage,
            '4':adminview.user_manage,
            '5':"back"
        }
        exit_flag = False
        while not exit_flag:
            print(menu)
            option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
            if option in menu_dict:
                if int(option) == len(menu_dict):
                    exit_flag = True
                else:
                    menu_dict[option](self)
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")
    def user_manage(self):
        admin.create_user(self)
    def school_manage(self):
        exit_flag = False
        menu = u'''
        ------- 校区管理菜单 ---------\033[32;1m
                1.  创建校区
                2.  返回\033[0m
        '''

        menu_dict = {
            '1':admin.create_school,
            '2':"back"
        }

        while not exit_flag:
            print(menu)
            option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
            if option in menu_dict:
                if int(option) == len(menu_dict):
                    exit_flag = True
                else:
                    menu_dict[option](self)
                    anwser = input("\033[31;1m是否继续创建校区？（Y/N)：\033[0m").strip()
                    if anwser == 'Y' or anwser == 'y':
                        continue
                    elif anwser == 'N' or anwser == 'n':
                        exit_flag =True
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")


    def course_manage(self):
        exit_flag = False
        menu = u'''
        ------- 课程管理菜单 ---------\033[32;1m
                1.  创建课程班级
                2.  返回\033[0m
        '''
        menu_dict = {
            '1':admin.create_course,
            '2':"back"
        }
        while not exit_flag:
            print(menu)
            option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
            if option in menu_dict:
                if int(option) == len(menu_dict):
                    exit_flag = True
                else:
                    menu_dict[option](self)
                    anwser = input("\033[31;1m是否继续创建课程？（Y/N)：\033[0m").strip()
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
                2.  返回\033[0m
        '''
        menu_dict = {
            '1':admin.invite_teacher,
            '2':"back"
        }
        while not exit_flag:
            print(menu)
            option = input("请输入菜单编号：").strip()
            if option in menu_dict:
                if int(option) == len(menu_dict):
                    exit_flag = True
                else:
                    menu_dict[option](self)
                    anwser = input("\033[31;1m是否继续添加讲师？（Y/N)：\033[0m").strip()
                    if anwser == 'Y' or anwser == 'y':
                        continue
                    elif anwser == 'N' or anwser == 'n':
                        exit_flag =True
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")


# 讲师视图
class teacherview(teacher):
    def __init__(self,teacher_name,teacher_salary,teacher_school,teacher_course):
        teacher.__init__(self,teacher_name,teacher_salary,teacher_school,teacher_course)
    def login(self):
        menu = u'''
       ------- 讲师主菜单 ---------
            \033[32;1m 1.  班级管理
            2.  成绩管理
            3.  返回
            \033[0m'''
        menu_dict = {
            "1":teacherview.class_manage,
            "2":teacherview.score_manage,
            "3":"back"
        }
        exit_flag = False
        while not exit_flag:
            print(menu)
            option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
            if option in menu_dict:
                if int(option) == len(menu_dict):
                    exit_flag = True
                else:
                    menu_dict[option](self)
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")

    def class_manage(self):
        menu = u'''
        ------- 班级管理 ---------\033[32;1m
                1.  查看班级学生人数
                2.  打印班级学生信息
                3.  返回\033[0m
        '''
        menu_dict = {
            "1": teacher.print_student,
            "2": teacher.print_student,
            "3": "back"
        }
        exit_flag = False
        while not exit_flag:
            print(menu)
            option = input("请输入菜单编号：").strip()
            if option in menu_dict:
                if int(option) == len(menu_dict):
                    exit_flag = True
                else:
                    menu_dict[option](self)
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")
    def score_manage(self):
        menu = u'''
        ------- 成绩管理 ---------\033[32;1m
                1.  登记学生成绩
                2.  修改学生成绩
                3.  查看学生成绩
                4.  返回\033[0m
        '''
        menu_dict = {
            "1": teacher.register_score,
            "2": teacher.update_score,
            "3": teacher.view_score,
            "4": "back"
        }
        exit_flag = False
        while not exit_flag:
            print(menu)
            option = input("请输入菜单编号：").strip()
            if option in menu_dict:
                if int(option) == len(menu_dict):
                    exit_flag = True
                else:
                    menu_dict[option](self)
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")

# 学生视图
class studentview(student):
    def __init__(self,student_name,student_sex,student_school,student_course,student_tution):
        student.__init__(self,student_name,student_sex,student_school,student_course,student_tution)
    def login(self):
        menu = u'''
       ------- 学生主菜单 ---------
            \033[32;1m 1.  注册
            2.  返回
            \033[0m'''
        menu_dict = {
            "1": studentview.register,
            "2": "back"
        }
        exit_flag = False
        while not exit_flag:
            print(menu)
            option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
            if option in menu_dict:
                if int(option) == len(menu_dict):
                    exit_flag = True
                else:
                    menu_dict[option](self)
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")
    def register(self):
        menu = u'''
        ------- 学员注册 --------\033[32;1m
                1.  学员注册
                2.  返回\033[0m
        '''
        menu_dict = {
            "1": student.student_register,
            "2": "back"
        }
        exit_flag = False
        while not exit_flag:
            print(menu)
            option = input("请输入菜单编号：").strip()
            if option in menu_dict:
                if int(option) == len(menu_dict):
                    exit_flag = True
                else:
                    menu_dict[option](self)
                    anwser = input("\033[31;1m是否继续注册学员？（Y/N)：\033[0m").strip()
                    if anwser == 'Y' or anwser == 'y':
                        continue
                    elif anwser == 'N' or anwser == 'n':
                        exit_flag =True
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")


class system(object):
    def __init__(self):
        pass
    def login(self):
        menu_dict = {
            "student": studentview,
            "teacher": teacherview,
            "admin": adminview
        }
        _username = input("请输入用户名：").strip()
        _password = input("请输入密码：").strip()
        # auth_status = auth(_username,_password)
        if os.path.isfile(user_file):
            with open(user_file,'r') as f:
                user_data = json.load(f)
            # if user_data['username'] == username and user_data['password'] == password:
            if _username in user_data.keys() and _password == user_data[_username]["password"]:
                print("用户登录成功！")
                if user_data[_username]["type"] == "admin":
                    print("欢迎进入管理视图！")
                    menu_dict["admin"].login(self)
                elif user_data[_username]["type"] == "teacher":
                    print("欢迎进入教师视图！")
                    menu_dict["teacher"].login(self)
                elif user_data[_username]["type"] == "student":
                    print("欢迎进入学生视图！")
                    menu_dict["student"].login(self)
            else:
                print("用户密码错误，登录失败！")