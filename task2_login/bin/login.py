#_*_coding:utf-8*_
#Author:Fiona

#读取用户信息表
import os,sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 文件路径配置
user_auth_file = os.path.join(os.path.sep,BASE_DIR,'file','user_auth.txt')
locked_file = os.path.join(os.path.sep,BASE_DIR,'file','locked_file.txt')
log_file = os.path.join(os.path.sep,BASE_DIR,'log','log.txt')

# 日志配置
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(log_file,encoding='utf-8')
handler.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# f = open(user_auth_file,"r",encoding="utf-8")
# user_passwd = f.readlines()
# f.close()
user_passwd=[]
with open(user_auth_file,"r",encoding="utf-8") as user_file:
    for line in user_file:
        user_passwd.append(line.strip())

#定义用户名列表和密码列表
user_dict = {}
username = []
password = []
locked_user = []    # 定义锁定用户数组
with open(locked_file,"r",encoding="utf-8") as lockeduser_file:
    for line in lockeduser_file:
        locked_user.append(line.strip())

for index,i in enumerate(user_passwd):
    if index%2 == 0:
        i=i.strip()
        username.append(i)
    else:
        i=i.strip()
        password.append(i)

user_dict = dict(zip(username,password))

#输入用户名
_username_ = input("username:")
#判断用户名是否在用户名列表中
if _username_ in user_dict.keys():

    #查找用户是否在黑名单
    count = 0
    if _username_ in locked_user:
            print("用户账号已锁定，请联系系统管理员。")
            logger.error(u'用户账号已锁定，请联系系统管理员。')
    else:
        while True:
            _password_ = input("password:")
            if _password_ == user_dict.get(_username_):
                print("用户登录成功！")
                logger.info(u'用户登录成功！')
                break
            elif _password_ != user_dict.get(_username_):
                count  += 1
                if count == 3:
                    print("用户密码连续输入错误3次，账号已锁定，请联系系统管理员解锁。")
                    logger.error(u'用户密码连续输入错误3次，账号已锁定，请联系系统管理员解锁。')
                    with open(locked_file,"a",encoding="utf-8") as add_lockeduser:
                        add_lockeduser.writelines("\n")
                        add_lockeduser.writelines(_username_)
                    break
                continue
else:
    print("用户名不存在！")
    logger.info(u'用户名不存在！')


try:
    raise Exception
except:
    logger.exception('exception')