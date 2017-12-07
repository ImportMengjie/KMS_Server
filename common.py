from flask import *
from  config import *
from model import *
from functools import wraps
import io
import struct
from fileToString import *


def typeList():
    return {
        "D0CF11E0": ('doc',handle_doc),
        "255044462D312E": ('pdf',handle_pdf),
        #"68746D6C3E":('html',handle_html),
        "504B030414": ('docx',handle_docx)
    }

CODES = ['UTF-8', 'UTF-16', 'GB18030', 'BIG5']
UTF_8_BOM = b'\xef\xbb\xbf'
# 字节码转16进制字符串
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()
# 获取文件类型
def filetype(file_bytes:bytes):
    binfile = io.BytesIO(file_bytes)
    tl = typeList()
    ftype = None
    for hcode in tl.keys():
        numOfBytes = len(hcode) // 2  # 需要读多少字节
        binfile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
        hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))  # 一个 "B"表示一个字节
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype

def string_encoding(b: bytes):
    for code in CODES:
        try:
            return b.decode(encoding=code)
        except Exception:
            continue
    return None

def auth_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.json.get('token')
        if not token:
            return jsonify(dic_comm_token_no_have), HTTP_Unauthorized
        u = User.objects(token=token).first()
        if not u:
            return jsonify(dic_comm_token_expired), HTTP_Unauthorized
        return func(user=u, *args, **kwargs)

    return wrapper


def get_dict(dic, add):
    return dict(dic, **add)



def handle_file(data):
    kind = filetype(data)
    if kind == None:
        string = None
        string=string_encoding(data)
        if string is None:
            raise TypeError('不支持的文件类型')
        return string,'txt'
    else:
        return kind[1](data),kind[0]

def handle_summary(text):
    return 'It is summary'

def handle_classify(data,summary=None,text=None):
    return Classify.objects().first()

def search_own(user,keyword):
    res = UserFile.objects(user=user).search_text(keyword)
    owntotal = len(res)
    ownfidlist = []
    ownnamelist = []
    owndatelist = []
    ownclassifylist = []
    ownsummarylist = []
    ownpublic = []
    for i in res:
        ownfidlist.append(str(i.id))
        ownnamelist.append(i.name)
        owndatelist.append(i.date)
        ownclassifylist.append(i.user_classify)
        ownsummarylist.append(i.file.summary)
        ownpublic.append(i.public)
    return get_dict(dic_comm_ok, {
        'owntotal': owntotal, 'ownfidlist': ownfidlist,
        'ownnamelist': ownnamelist, 'owndatelist': owndatelist,
        'ownclassifylist': ownclassifylist, 'ownsummarylist': ownsummarylist, 'ownpublic': ownpublic})


def search_other(user,keyword):
    res = UserFile.objects(user__ne=user,public=True).search_text(keyword)
    total = len(res)
    fidlist = []
    namelist = []
    datelist = []
    classifylist = []
    summarylist = []
    userid = []
    username=[]
    for i in res:
        fidlist.append(i.id)
        namelist.append(i.name)
        datelist.append(i.date)
        classifylist.append(i.user_classify)
        summarylist.append(i.file.summary)
        userid.append(str(i.user.id))
        username.append(i.user.name)
    return get_dict(dic_comm_ok, {
        'total': total, 'fidlist': fidlist,
        'namelist': namelist, 'datelist': datelist,
        'classifylist': classifylist, 'summarylist': summarylist, 'userid': userid,
        'username':username})


