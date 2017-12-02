import requests
import base64
import io
import model
import filetype

url = 'http://localhost:5000/'
token = '3fceab95b1e7544bfe2c8886f50da0941fc9a531'
#token='202f4a91a986dacb1d32e9839c9f870447425f65'

# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少半2字符，长则8字符
def typeList():
    return {
        "D0CF11E0": 'doc',
        "255044462D312E": 'pdf',
        "3C3F786D6C":'xml',
        "68746D6C3E":'html',
        "7B5C727466":'rtf'}
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
def filetype2(filename):
    binfile = open(filename, 'rb')  # 必需二制字读取
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

def testfiletype():
    print(filetype.guess('1'))


def uploadfile(name,filename):
    with open(filename, 'rb') as f:
        data = f.read()
        print(data)
        data = base64.b64encode(data)
        payload = {'token': token, 'data': str(data, 'utf-8'), 'name': name,
                   'public': True}
        req = requests.post(url + 'app/user/upload', json=payload)
        print(req.json())

def modifyinfo():
    payload={'token':token,'name':'杨佳宇'}
    req = requests.post(url + 'app/user/modifyinfo', json=payload)
    print(req.text)

def getfile():
    id = '5a192ea7dee17115ae90c994'
    payload = {'token': token, 'fid': id}
    req = requests.post(url + 'app/user/getfile', json=payload)
    print(req.text)


def modifyfile():
    id = '5a19038fdee17116885cacc2'
    payload = {'token': token, 'fid': id, 'name': '我是sb', 'delete': True}
    req = requests.post(url + 'app/user/modifyfile', json=payload)
    print(req.json())


def getownfilelist():
    payload = {'token': token}
    req = requests.get(url + 'app/user/getownfilelist', json=payload)
    print(req.json())

def getfilelist():
    payload = {'token': token}
    req = requests.post(url + 'app/user/getfilelist', json=payload)
    print(req.json())

def favorite():
    payload = {'token': token, 'fid': '5a19427ddee1711ff16b8588','cancel':True}
    req = requests.post(url + 'app/user/favorite', json=payload)
    print(req.json())

def search():
    payload = {'token': token, 'keyword': '是'}
    req = requests.post(url + 'app/user/search', json=payload)
    print(req.json())

#testfiletype()
# modifyinfo()
#uploadfile('sbsbsbs我是sb啊','1')
# uploadfile('我是doc,s李大帅b333,我是你爸爸','1.doc')
# uploadfile('我是一章pdf我3李大帅321是你爷爷','1.pdf')
# uploadfile('我是一张图片狗12李大帅1我是sb','1.png')
#getfile()
# modifyfile()
# getownfilelist()
#favorite()
#getfilelist()
search()