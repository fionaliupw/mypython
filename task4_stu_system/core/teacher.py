#_*_coding:utf-8*_
#Author:Fiona

import sys
from conf.settings import BASE_DIR
from .models import Teacher,School,Student,Study_score,Class,Class_course,Course,User
sys.path.append(BASE_DIR)
sys.path.append("..")

class Teacherview(object):
    def __init__(self,session):
        self.session = session
        # self.run()

    # def run(self):
    #     menu = u'''
    #    ------- 讲师主菜单 ---------
    #         \033[32;1m 1.  添加班级
    #         2.  添加课程
    #         3.  注册学员
    #         4.  添加成绩
    #         5.  修改成绩
    #         b.  返回
    #         \033[0m'''
    #     teacher_name = input("\033[34;0m请输入班级讲师的姓名：\033[0m")
    #     self.teacher_obj = self.session.query(Teacher).filter_by(teacher_name=teacher_name).first()
    #     exit_flag = False
    #     while not exit_flag:
    #         print(menu)
    #         option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
    #         if option == 'b':
    #             exit()
    #         elif option == '1':
    #             Teacherview.class_manage(self)
    #         elif option == '2':
    #             Teacherview.course_manage(self)
    #         elif option == '3':
    #             Teacherview.add_student(self)
    #         elif option == '4':
    #             Teacherview.add_score(self)
    #         elif option == '5':
    #             Teacherview.modify_score(self)
    #         else:
    #             print("\033[31;1m菜单编号不存在，请重新输入\033[0m")
    def class_manage(self,teacher_obj):
        exit_flag = False
        menu = u'''
        ------- 班级管理菜单 ---------\033[32;1m
                1.  创建班级
                b.  返回\033[0m
        '''
        while not exit_flag:
            print(menu)
            option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
            if option == 'b':
                exit_flag = True
            elif option == '1':
                class_name = input("\033[34;0m请输入创建班级的名称：\033[0m")
                course_name = input("\033[34;0m请输入创建班级的课程:\033[0m")
                class_obj = self.session.query(Class).filter_by(class_name=class_name).first()
                course_obj = self.session.query(Course).filter_by(course_name=course_name).first()
                if not course_obj:
                    course_new = Course(course_name=course_name)
                    self.session.add(course_new)
                    self.session.commit()
                if not class_obj:
                    class_new = Class(class_name=class_name,course=course_name)
                    teacher_obj.classes.append(class_new)
                    self.session.add(class_new)
                    self.session.commit()
                    print("\033[34;1m班级创建成功\033[0m")
                relation = self.session.query(Class_course).filter(Class_course.class_id==class_new.class_id).filter(Class_course.course_id==course_new.course_id).first()
                if not relation:
                    Class_Course_new = Class_course(class_id=class_new.class_id,course_id=course_new.course_id)
                    self.session.add(Class_Course_new)
                    self.session.commit()
                else:
                    print("\33[31;1m班级创建失败，该班级已经存在！\33[0m")
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")

    def course_manage(self,teacher_obj):
        exit_flag = False
        menu = u'''
        ------- 课程管理菜单 ---------\033[32;1m
                1.  创建课程
                b.  返回\033[0m
        '''
        while not exit_flag:
            print(menu)
            option = input("\033[31;1m请输入菜单编号：\033[0m").strip()
            if option == 'b':
                exit_flag = True
            elif option == '1':
                course_name = input("\033[34;0m请输入创建的课程：\033[0m")
                course_obj = self.session.query(Course).filter_by(course_name=course_name).first()
                if not course_obj:
                    course_new = Course(course_name=course_name)
                    self.session.add(course_new)
                    self.session.commit()
            else:
                print("\033[31;1m菜单编号不存在，请重新输入\033[0m")

    def add_score(self,teacher_obj):
        for view_classtable in self.session.query(Class.class_id.label('class_id'),Class.class_name.label('class_name'),
                                                  Class.course.label('course')).all():
            print(view_classtable.class_id,view_classtable.class_name,view_classtable.course)
        class_name = input("\033[34;0m请输入要添加学习记录的班级名：\033[0m")
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()
        if class_obj and class_obj.teacher[0] == teacher_obj:
            course_name = input("\033[34;0m请输入添加学习记录的课程名（course）:\033[0m")
            course_obj = self.session.query(Course).filter_by(course_name=course_name).first()
            if course_obj:
                class_course_obj = self.session.query(Class_course).filter(Class_course.class_id == class_obj.class_id).filter(Class_course.course_id == course_obj.course_id).first()
                if class_course_obj:
                    study_score_obj = self.session.query(Study_score).filter_by(class_course_id=class_course_obj.id).first()
                    if not study_score_obj:
                        for student_obj in class_obj.students:

                            score = input("输入学生 %s 的 %s 学习成绩："% (student_obj.student_name,course_obj.course_name))
                            study_score_new = Study_score(class_course_id=class_course_obj.id,
                                                            student_id=student_obj.student_id,
                                                            score=score)
                            self.session.add(study_score_new)
                            self.session.commit()
                    else:
                        print("\33[31;1m当前上课记录已经创建\33[0m")
                else:
                     print("\33[31;1m当前班级的class_course未创建\33[0m")
            else:
                print("\33[31;1m课程course未创建\33[0m")
        else:
            print("\33[31;1m班级不存在或没有权限管理此班级\33[0m")
    def modify_score(self,teacher_obj):
        score_obj = self.session.query(Study_score.id.label('study_score_id'),Class.class_name.label('class_name'),
                                       Course.course_name.label('course_name'),Student.student_name.label('student_name'),
                                       Study_score.score.label('score')).filter(Student.student_id==Study_score.student_id).\
            filter(Class_course.id==Study_score.class_course_id).\
            filter(Class.class_id==Class_course.class_id).\
            filter(Course.course_id==Class_course.course_id).all()
        for view_score in  score_obj:
            print(view_score.study_score_id,view_score.class_name,view_score.course_name,view_score.student_name,view_score.score)

        class_name = input("\033[34;0m请输入学习记录的班级名:\033[0m")
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()
        if class_obj and class_obj.teacher[0] == teacher_obj:
            course_name = input("\033[34;0m请输入学习记录的课节名（course）:\033[0m")
            course_obj = self.session.query(Course).filter_by(course_name=course_name).first()
            if course_obj:
                class_course_obj = self.session.query(Class_course).filter(
                    Class_course.class_id == class_obj.class_id).filter(Class_course.course_id == course_obj.course_id).first()
                if class_course_obj:
                    # exit_flag = False
                    # while not exit_flag:
                    study_score_objs = self.session.query(Study_score).filter(Study_score.class_course_id==class_course_obj.id).all()
                    for obj in study_score_objs:
                        print(obj)
                    student_name = input("\033[34;0m输入要修改成绩的学生名：[Q 退出]\33[0m")
                    student_obj = self.session.query(Student).filter_by(student_name=student_name).first()
                    if student_obj:
                        study_score_obj = self.session.query(Study_score).filter(Study_score.class_course_id==class_course_obj.id).filter(Study_score.student_id == student_obj.student_id).first()
                        if study_score_obj:
                            score = input("\033[34;0m输入修改后的成绩:\33[0m")
                            study_score_obj.score= score
                            self.session.commit()
                        else:
                            print("\33[31;1m当前学生学习成绩未添加\33[0m")
                    else:
                        print("\33[31;1m当前学生未注册\33[0m")
                else:
                    print("\33[31;1m当前班级的课程未创建\33[0m")
            else:
                print("\33[31;1m课程course未创建\33[0m")
        else:
            print("\33[31;1m班级不存在或没有权限管理此班级\33[0m")
    def add_student(self,teacher_obj):
        for view_classtable in self.session.query(Class.class_id.label('class_id'),Class.class_name.label('class_name'),
                                                  Class.course.label('course')).all():
            print(view_classtable.class_id,view_classtable.class_name,view_classtable.course)
        class_name = input("\033[34;0m请输入要注册的班级名：\033[0m")
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()
        if class_obj and class_obj.teacher[0] == teacher_obj:
            stu_name = input("\033[34;0m请输入学员的姓名:\033[0m")
            student_obj = self.session.query(Student).filter_by(student_name=stu_name).first()
            if not student_obj:
                student_new = Student(student_name=stu_name)
                class_obj.students.append(student_new)
                self.session.add(student_new)
                self.session.commit()
                print("\033[34;1m学员添加注册\033[0m")
            else:
                print("\33[31;1m学员已经存在\33[0m")
        else:
            print("\33[31;1m班级不存在或没有权限管理此班级\33[0m")