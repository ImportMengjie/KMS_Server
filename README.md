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
            'msg':(string)
        }

## 返回值:code && msg && HTTP stat code

通用(0~99)

code | msg | HTTP
---|---|---
0 | 成功 | HTTP_OK
1 | 格式错误 | HTTP_Bad_Request
2 | 没找到该资源 | HTTP_NotFound
3 | token过期 | HTTP_Unauthorized
4 | 没有token | HTTP_Unauthorized
5 | 服务器内部出错 | HTTP_Server_Error

---
           
### 注册:

code | msg | HTTP
---|---|---
100 | 注册成功 | HTTP_Created
101 | 该手机号已被注册(跳转登录?) | HTTP_Forbidden
102 | 该手机号未被注册 | HTTP_OK   
 

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

code | msg | HTTP
---|---|---
110 | 登录成功 | HTTP_OK
111 | 没找到此用户 | HTTP_NotFound
112 | 密码错误 | HTTP_Forbidden

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

### 查看热门

    # 查看热门
    route:
        /app/see,methods=['Get']
    required:
    {
    
    }
    return:
        {
        'total':(long),
        'tag':(long),
        'fidlist':[(string),,,],
        'namelist':[(string),,,],
        'datelist':[(long),,,],
        'classfiylist':[(string),,,],
        'summarylist':[(string),,,],
        'username':(string),
        'userid':(string) 
        }

---
以下需要传入token,可能会产生的code(3,4)

  
### 头像?

code | msg | HTTP
---|---|---
120 | 上传成功 | HTTP_Created
121 | 获取头像成功 | HTTP_OK

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
        '/app/user/get_avatar', methods=['Get']
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

code | msg | HTTP
---|---|---
130 | 上传成功 | HTTP_Created
131 | 创建成功 | HTTP_Created

    # 上传文件
    route:
        '/app/user/upload', methods=['Post']
    1. 验证文件是否在数据库已经存在
    required:
    {
        'md5':(string) # 文件的md5码
        'name':(string) # 文件的title
        'public':(bool) # 是否公开
    }
    return:
    code(2,131)
    if code==131:
    {
        fid=(string) #以后获取该资源发送fid获取
        classify:(string) # 推荐分类
        summary:(string) # 摘要
    }

    2. 文件若是不存在上传文件
    required:
    {
        'name':(string) # 文件的title
        'data':(strin) # 文件的data
        'public':(bool)# 是否公开
    }
    return:
    code(130)
    {
        fid=(string) #以后获取该资源发送fid获取
        classify:(string) # 推荐分类
        summary:(string) # 摘要
    }
    
    

### 获取文件,修改文件

code | msg | HTTP
---|---|---
140 | 获取成功 | HTTP_OK
141 | 修改成功 | HTTP_OK
142 | 删除成功 | HTTP_OK
143 | 没有修改 | HTTP_Forbidden

    ＃ 获取文件
    route:
        '/app/user/getfile', methods=['Get']
    required:
    {
        'fid':(string)
    }
    return:
    code(140,2)
    if code==140:
    {
        'data':(string),
        'name':(string),
        'summary':(string),
        'classify':(string),
    }
    
    # 修改文件
    route:
        '/app/user/modifyfile', methods=['Post']
    required:
    {
        'fid':(string),
        'public':(bool),
        'name':(string),
        'classify':(string) # 修改的分类
        'delete':(bool) # 是否删除
    }
    return:
    code(142,143)
 
    


### 修改用户信息

code | msg | HTTP
---|---|---
150 | 修改成功 | HTTP_OK
151 | 没有任何改变 | HTTP_Forbidden

    # 修改用户信息,如果其中一项没有修改不传即可
    route:
        '/app/user/modifyinfo', methods=['POST']
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
        '/app/user/info', methods=['Get']
    required:
    {
        'userid':(string) # 如果没有此项则获取自己的信息
    }
    return:
    code(2,0)
    {
        'name':(string),
        'phone',(string),
        'email',(string),
        'birth',(string)
    }

### 获取自己文件列表
    # 获取自己编写的文件列表
    route:
        '/app/user/getownfilelist', methods=['Get']
    required:
    {
    
    }
    return:
    {
        'total':(long),
        'fidlist':[(string),,,],
        'namelist':[(string),,,],
        'datelist':[(long),,,],
        'classfiylist':[(string),,,],
        'summarylist':[(string),,,]
        'public':[(bool),,,]# 是否公开
        
    }
    
### 获取推荐列表
    # 获取推荐文件列表
    route:
        '/app/user/getfilelist',methods=['Get']
    required:
    {
    
    }
    return:
    {
        'total':(long),
        'tag':(long),
        'fidlist':[(string),,,],
        'namelist':[(string),,,],
        'datelist':[(long),,,],
        'classfiylist':[(string),,,],
        'summarylist':[(string),,,],
        'username':(string),
        'userid':(string)
    }
  
### 收藏

code | msg | HTTP
---|---|---
160 | 收藏成功 | HTTP_OK
161 | 已经收藏过了 | HTTP_Forbidden
162 | 取消收藏成功 | HTTP_OK
163 | 它不是你的收藏 | HTTP_Forbidden
    
    # 收藏
    route:
        '/app/user/favorite',methods=['Post']
    required:
    {
        'fid':(string)
    }
    return:
    {
        'fid':(string) #新收藏的fid
    }
    code(160,161)
    
    # 取消收藏
    route:
        '/app/user/favorite',methods=['Post']
    required:
    {
        'fid':(string)
        'cancel':(bool)
    }
    return:
    code(162,163)
    
    # 获取用户收藏列表
    route:
        '/app/user/favorite',methods=['Post']
    required:
    {
    
    }
    return:
    {
        'total':(long),
        'fidlist':[(string),,,],
        'namelist':[(string),,,],
        'datelist':[(long),,,],
        'classfiylist':[(string),,,],
        'summarylist':[(string),,,],
        'username':(string),
        'userid':(string)
    } 
    
# 搜索
code | msg | HTTP
---|---|---
170 | 搜索成功 | HTTP_OK
    
    #搜索
    route:
       '/app/user/search',methods=['Post']
    required:
    {
        'keyword':(string)
    }
    return:
    {
        # 自己的文件列表,包括收藏的
        'owntotal':(long),
        'ownfidlist':[(string),,,],
        'ownnamelist':[(string),,,],
        'owndatelist':[(long),,,],
        'ownclassfiylist':[(string),,,],
        'ownsummarylist':[(string),,,],
        'ownpublic':[(bool),,,],
        
        # 他人的文件列表
        'total':(long),
        'fidlist':[(string),,,],
        'namelist':[(string),,,],
        'datelist':[(long),,,],
        'classfiylist':[(string),,,],
        'summarylist':[(string),,,],
        'username':(string),
        'userid':(string)
    }
    



    
    
    