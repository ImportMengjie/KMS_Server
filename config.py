from model import *

# mongodb configuration
MONGODB_SETTINGS = {
    'db': 'mydata',
    'host': '127.0.0.1',
}

# HTTP stat
# 200
HTTP_OK = 200  # 请求成功。一般用于GET与POST请求
HTTP_Created = 201  # 已创建。成功请求并创建了新的资源
HTTP_Accepted = 202  # 已接受。已经接受请求，但未处理完成
HTTP_No_Content = 204  # 无内容。服务器成功处理，但未返回内容
HTTP_Partial_Content = 206  # 部分内容。服务器成功处理了部分GET请求

# 400
HTTP_Bad_Request = 400  # 客户端请求的语法错误，服务器无法理解
HTTP_Unauthorized = 401  # 请求要求用户的身份认证
HTTP_Forbidden = 403  # 服务器理解请求客户端的请求，但是拒绝执行此请求

# 500
HTTP_Server_Error = 500  # 服务器内部错误，无法完成请求

json_success = 'done'
json_msg = 'msg'


msg_format_error = '格式错误'
msg_server_error = '服务器发生错误'

msg_has_been_register = '该用户已经被注册了'
msg_register_success = '注册成功'

msg_login_NotFound = 0
msg_login_pw_error = '密码错误!'
msg_login_success = '登录成功'

msg_modify_success = '更改成功'

msg_auth_need = '请登录!'
msg_auth_require = '需要登录'

msg_file_notfound = '没找到文件'
msg_file_nodata = '没有文件'
msg_file_upload_ok = '上传成功'