# KMS_Server

## 通用:

    HTTP stat:
        HTTP_OK = 200  # 请求成功,并且处理无错误
        HTTP_Created = 201  # 已创建。成功请求并创建了新的资源
        HTTP_Accepted = 202  # 已接受。已经接受请求，但未处理完成
        HTTP_Partial_Content = 206  # 部分内容。服务器成功处理了部分GET请求

        # 400
        HTTP_Bad_Request = 400  # 客户端请求的语法错误，服务器无法理解
        HTTP_Unauthorized = 401  # 请求要求用户的身份认证
        HTTP_Forbidden = 403  # 服务器理解请求客户端的请求，但是拒绝执行此请求
        HTTP_NotFound = 404 # 没找到

        # 500
        HTTP_Server_Error = 500  # 服务器内部错误，无法完成请求


    return json format:
        {
            //必返回项
            'done':(bool),
            'code':(int),
            'msg':(string),
            <!--// 可选项-->
            <!--'data':(string), # base64编码-->
            <!--'fid':(string), # 文件id-->
        }

## 返回值:code && msg && HTTP stat code

0. 通用(0~99)

code | msg | HTTP
---|---|---
1 | 格式错误 | HTTP_Forbidden
2 | 没找到该资源 | HTTP_NotFound
3 | token过期 | HTTP_Forbidden
4 | 没有token | HTTP_Forbidden



1. 注册(100~109)

code | msg | HTTP
---|---|---
100 | 注册成功 | HTTP_Created
101 | 该手机号已被注册(跳转登录?) | HTTP_Forbidden
102 | 该手机号未被注册 | HTTP_OK



2. 登录(110~119)

code | msg | HTTP
---|---|---
110 | 登录成功 | HTTP_OK
111 | 没找到此用户 | HTTP_NotFound
112 | 密码错误 | HTTP_Forbidden


3. 头像(120~129)

code | msg | HTTP
---|---|---
120 | 上传成功 | HTTP_Created
121 | 获取头像成功 | HTTP_OK


4. 上传文件(130~139)

code | msg | HTTP
---|---|---
130 | 上传成功 | HTTP_Created
131 | 创建成功 | HTTP_Created


5. 获取文件(140~149)

code | msg | HTTP
---|---|---
140 | 获取成功 | HTTP_OK


6. 修改用户信息(150~159)

code | msg | HTTP
---|---|---
150 | 修改成功 | HTTP_OK
151 | 没有任何改变 | HTTP_Forbidden



### 注册:

    # 注册
    route:
        '/app/register', methods=['Post']
    requires:
    {
        'phone':(string,required=True), # 手机号
        'name':(string,required=True,maxlength=16), # 名字
        'email':(string,required=False,maxlength=55), #邮箱
        'password':(string,required=True,maxlength=16), #密码
        'birth':(long,required=False), # 生日
    }

    return:
        code(100,101,1)

    # 验证手机号是否已经被注册
    route:
        '/app/register/testphone', methods=['Post']
    requires:
    {
        'phone':(string,required=True), # 手机号
    }

    return:
        code(101,102,1)


### 登录:
    # 登录:
    route:
        '/app/login', methods=['Post']
    required:
    {
        'phone':(string,required=True),
        'password':(string,required=True,maxlength=16), #密码
    }
    return:
        code(110,111,112,1)e

        if code==110:
            {
                'first_time':(bool) # 该用户是否是第一次登录
                'token':(string) #以后每次发送请求都要带上token,并且应该保存在客户端
            }


---
以下需要传入token,可能会产生的code(3,4)


### 头像?
    # 上传头像
    route:
        /app/user/avatar', methods=['Post']
    required:
    {
        'data':(string), # base64编码的头像文件
        'token':(string)
    }
    return:
        code(1,120)

    # 获取头像
    route:
        '/app/user/get_avatar', methods=['Post']
    required:
    {

    }
    return:
     code(2,121)
     if code==121:
    {
        'data':(string)
    }

### 上传文件
    # 上传文件
    route:
        '/app/user/upload', methods=['Post']
    1. 验证文件是否在数据库已经存在
    required:
    {
        'md5':(string) # 文件的md5码
        'name':(string) # 文件的title
    }
    return:
    code(2,131)
    if code==131:
    {
        fid=(string) #以后获取该资源发送fid获取
    }

    2. 文件若是不存在上传文件
    required:
    {
        'name':(string) # 文件的title
        'data':(strin) # 文件的data
    }
    return:
    code(130)
    {
        fid=(string) #以后获取该资源发送fid获取
    }

### 获取文件
    ＃ 获取文件
    route:
        '/app/user/getfile', methods=['Post']
    required:
    {
        'fid':(string)
    }
    return:
    code(140,2)
    if code==140:
    {
        'data':(string)
        'name':(string)
    }


### 修改用户信息
    # 修改用户信息,如果其中一项没有修改不传即可
    route:
        '/app/user/modify', methods=['POST']
    required:
    {
        'name':(string)
        'password':(string),
        'birth';(long)
    }
    return:
    code(150,151)

### 获取用户信息
    # 获取用户信息
    route:
        '/app/user/info', methods=['POST']
    required:
    {

    }
    return:
    {
        'name':(string),
        'phone',(string),
        'email',(string),
        'birth',(string)
    }

### 获取自己文件列表
    # 获取自己文件列表
    route:
        '/app/user/getownfilelist', methods=['POST']
    required:
    {
    
    }
    return:
    {
        'fidlist':[(string),,,],
        'namelist':[(string),,,],
        'datelist':[(long),,,],
        
        
    }
    
### 获取推荐列表
    # 获取推荐文件列表
    route:
        '/app/user/getfilelist',methods=['Post']
    required:
    {
    
    }
    return:
    {
    
    }
    