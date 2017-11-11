from model import *

from enum import Enum, unique

# mongodb configuration
MONGODB_SETTINGS = {
    'db': 'mydata',
    'host': '127.0.0.1',
}


def _getdic(msg,code):
    return {'code':code,'msg':msg}
# comm
dic_comm_format_error=_getdic("格式错误",1)
dic_comm_not_found = _getdic('没找到该资源',2)
dic_comm_token_expired = _getdic('token过期',3)
dic_comm_token_no_have = _getdic('没有token',4)
#register
dic_register_success = _getdic('注册成功',100)
dic_register_has_been_register = _getdic('该手机号已被注册',101)
dic_register_isok_register = _getdic('该手机号未被注册',102)
#login
dic_login_success = _getdic("登录成功",110)
dic_login_notfound = _getdic("没找到此用户",111)
dic_login_pw_erro = _getdic("密码错误",112)
#avatar
dic_avatar_ok = _getdic("上传成功",120)
dic_avatar_get_ok = _getdic("获取头像成功",121)
#upload
dic_upload_ok = _getdic("上传文件成功",130)
dic_upload_create_ok=_getdic("创建文件成功",131)
#file
dic_file_get_ok=_getdic("获取文件成功",140)
dic_file_modify_ok = _getdic("修改成功",141)
dic_file_dele_ok = _getdic("删除成功",142)
dic_file_modify_none = _getdic("没有修改",143)
#modify
dic_modify_ok = _getdic('修改成功',150)
dic_modify_none = _getdic("没有任何改变",151)
#favorite
dic_favorite_ok = _getdic('收藏成功',160)
dic_favorite_has_been = _getdic('已经收藏过了',161)
dic_favorite_cancel = _getdic('取消收藏',162)
dic_favorite_it_not_your = _getdic('它不是你的收藏',163)


