#_*_coding:utf-8*_
#Author:Fiona

import os,sys,json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

user_file = os.path.join(os.path.sep,BASE_DIR,'data','user.json')
# locked_file = os.path.join(os.path.sep,BASE_DIR,'data','locked_user.txt')

# # 读取用户信息
# with open(user_file,'r+') as read_user:
#     user_dict = json.loads(read_user.read())

# # 读取被锁用户信息
# locked_user = []    # 定义锁定用户数组
# with open(locked_file,"r",encoding="utf-8") as lockeduser_file:
#     for line in lockeduser_file:
#         locked_user.append(line.strip())

def login():
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
                pass
            elif user_data[_username]["type"] == "teacher":
                print("欢迎进入教师视图！")
                pass
            elif user_data[_username]["type"] == "student":
                print("欢迎进入学生视图！")
                pass
        else:
            print("用户密码错误，登录失败！")

login()

# print(user_dict.keys())
# if len(_username) > 0:
#     if _username in user_dict.keys():
#         if _username in locked_user:
#             print("用户账号已锁定，请联系系统管理员。")
#         else:
#             while True:
#                 _password = input("请输入登录密码：").strip()
#                 fail_count = 0
#                 if _password == user_dict[_username]["password"]:
#                     print("用户登录成功！")
#
#                     break
#                 else:
#                     fail_count += 1
#                     if fail_count == 3:
#                         print("用户密码连续输入错误3次，账号已锁定，请联系系统管理员解锁。")
#                         with open(locked_file,'a') as write_locked:
#                             write_locked.writelines("\n")
#                             write_locked.writelines(_username)
#                         break
#                     continue
