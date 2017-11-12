from model import *

from enum import Enum, unique

# mongodb configuration
MONGODB_SETTINGS = {
    'db': 'mydata',
    'host': '127.0.0.1',
}

HTTP_OK = 200  # 请求成功,并且处理无错误
HTTP_Created = 201  # 已创建。成功请求并创建了新的资源
HTTP_Accepted = 202  # 已接受。已经接受请求，但未处理完成
HTTP_Partial_Content = 206  # 部分内容。服务器成功处理了部分GET请求

# 400
HTTP_Bad_Request = 400  # 客户端请求的语法错误，服务器无法理解
HTTP_Unauthorized = 401  # 请求要求用户的身份认证
HTTP_Forbidden = 403  # 服务器理解请求客户端的请求，但是拒绝执行此请求
HTTP_NotFound = 404  # 没找到

# 500
HTTP_Server_Error = 500  # 服务器内部错误，无法完成请求


def _getdic(msg,code,done):
    return {'code':code,'msg':msg,'done':done}
# comm
dic_comm_ok = _getdic("完成",0,True)
dic_comm_format_error=_getdic("格式错误",1,False)
dic_comm_not_found = _getdic('没找到该资源',2,False)
dic_comm_token_expired = _getdic('token过期',3,False)
dic_comm_token_no_have = _getdic('没有token',4,False)
dic_comm_server_error = _getdic('服务器内部错误',5,False)
#register
dic_register_success = _getdic('注册成功',100,True)
dic_register_has_been_register = _getdic('该手机号已被注册',101,False)
dic_register_isok_register = _getdic('该手机号未被注册',102,True)
#login
dic_login_success = _getdic("登录成功",110,True)
dic_login_notfound = _getdic("没找到此用户",111,False)
dic_login_pw_erro = _getdic("密码错误",112,False)
#avatar
dic_avatar_ok = _getdic("上传成功",120,True)
dic_avatar_get_ok = _getdic("获取头像成功",121,True)
#upload
dic_upload_ok = _getdic("上传文件成功",130,True)
dic_upload_create_ok=_getdic("创建文件成功",131,True)
#file
dic_file_get_ok=_getdic("获取文件成功",140,True)
dic_file_modify_ok = _getdic("修改成功",141,True)
dic_file_dele_ok = _getdic("删除成功",142,True)
dic_file_modify_none = _getdic("没有修改",143,False)
#modify
dic_modify_ok = _getdic('修改成功',150,True)
dic_modify_none = _getdic("没有任何改变",151,False)
#favorite
dic_favorite_ok = _getdic('收藏成功',160,True)
dic_favorite_has_been = _getdic('已经收藏过了',161,False)
dic_favorite_cancel = _getdic('取消收藏',162,True)
dic_favorite_it_not_your = _getdic('它不是你的收藏',163,False)
# search
dic_search_ok = _getdic('搜索成功',170,True)

