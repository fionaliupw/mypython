#_*_coding:utf-8*_
#Author:Fiona
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,ForeignKey,Table,Float
from sqlalchemy.orm import relationship
from conf.settings import engine

# 生成ORM基类
Base  = declarative_base()

# 老师 班级 对应关系表
teacher2class = Table("teacher_class",Base.metadata,
                      Column("teacher_id",Integer,ForeignKey("teacher.teacher_id")),
                      Column("class_id",Integer,ForeignKey("classes.class_id"))
                      )

# 班级 学生 对应关系表
class2student = Table("class_student",Base.metadata,
                      Column("class_id",Integer,ForeignKey("classes.class_id")),
                      Column("student_id",Integer,ForeignKey("student.student_id"))
                      )

# 班级 课程对应关系表
class Class_course(Base):
    __tablename__ = "class_course"
    id = Column(Integer,primary_key=True)
    class_id = Column(Integer,ForeignKey("classes.class_id"))
    course_id = Column(Integer,ForeignKey("course.course_id"))

    classes = relationship("Class",backref="class_courses")
    courses = relationship("Course",backref="class_courses")

    def __repr__(self):
        return "<%s %s>" % (self.classes,self.courses)

# 管理员
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer,primary_key=True,nullable=False)
    username = Column(String(50),nullable=False)
    password = Column(String(25),nullable=False)
    user_type = Column(String(25),nullable=False)

    def __repr__(self):
        return "<User(username='%s',password='%s',user_type='%s')>" % (self.username,self.password,self.user_type)

# 学校
class School(Base):
    __tablename__ = 'school'
    school_id = Column(Integer,primary_key=True,nullable=False)
    school_name = Column(String(50),nullable=False)
    address = Column(String(255))
    ext_1 = Column(String(100))
    ext_2 = Column(String(100))
    ext_3 = Column(String(100))

    def __repr__(self):
        return "<School(school_name='%s',location='%s')>" % (self.school_name,self.location)

# 老师
class Teacher(Base):
    __tablename__ = 'teacher'
    teacher_id = Column(Integer,primary_key=True,nullable=False)
    teacher_name = Column(String(50),nullable=False)
    ext_1 = Column(String(100))
    ext_2 = Column(String(100))
    ext_3 = Column(String(100))

    classes = relationship("Class",secondary=teacher2class,backref="teacher")

    def __repr__(self):
        return "<Teacher(teacher_name='%s')>" % self.teacher_name

# 学生
class Student(Base):
    __tablename__ = 'student'
    student_id = Column(Integer,primary_key=True,nullable=False)
    student_name = Column(String(50),nullable=False)
    tuition = Column(Float)
    ext_2 = Column(String(100))
    ext_3 = Column(String(100))

    def __repr__(self):
        return "<Student(student_name='%s')>" % self.student_name

# 学习成绩表
class Study_score(Base):
    __tablename__ = "study_score"
    id = Column(Integer,primary_key=True,nullable=False)
    class_course_id = Column(Integer,ForeignKey("class_course.id"))
    student_id = Column(Integer,ForeignKey("student.student_id"))
    score = Column(Integer,nullable=True)

    class_courses = relationship("Class_course",backref="my_study_score")
    students = relationship("Student",backref="my_study_score")

    def __repr__(self):
        return "\033[35;0m%s,%s,成绩：【%s】\33[0m" % (self.class_courses,self.students,self.score)

# 课程
class Course(Base):
    __tablename__ = 'course'
    course_id = Column(Integer,primary_key=True,nullable=False)
    course_name = Column(String(50),nullable=False)
    ext_1 = Column(String(100))
    ext_2 = Column(String(100))
    ext_3 = Column(String(100))

    def __repr__(self):
        return "<Course(course_name='%s')>" % self.course_name

# 班级
class Class(Base):
    __tablename__ = 'classes'
    class_id = Column(Integer,primary_key=True,nullable=False)
    class_name = Column(String(25),nullable=False)
    course = Column(String(50),nullable=False)
    ext_1 = Column(String(100))
    ext_2 = Column(String(100))
    ext_3 = Column(String(100))

    students = relationship("Student",secondary=class2student,backref="classes")

    def __repr__(self):
        return "<Class(class_name='%s')>" % self.class_name

Base.metadata.create_all(engine)