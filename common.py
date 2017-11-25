from flask import *
from  config import *
from model import *
from functools import wraps
import filetype
import io


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
    with open('/home/mengjie/1','wb+') as f:
        f.write(data)
    kind = filetype.guess(data)
    if kind == None:
        raise TypeError
    print(kind.extension)
    return kind.MIME

def handle_summary(data):
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
        ownfidlist.append(i.id)
        ownnamelist.append(i.name)
        owndatelist.append(i.date)
        ownclassifylist.append(i.user_classify)
        ownsummarylist.append(i.file.summary)
        ownpublic.append(i.public)
    return jsonify(get_dict(dic_comm_ok, {
        'owntotal': owntotal, 'ownfidlist': str(ownfidlist),
        'ownnamelist': ownnamelist, 'owndatelist': owndatelist,
        'ownclassifylist': ownclassifylist, 'ownsummarylist': ownsummarylist, 'ownpublic': ownpublic}))


def search(user,keyword):
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
        fidlist.append(str(i.id))
        namelist.append(i.name)
        datelist.append(i.date)
        classifylist.append(i.user_classify)
        summarylist.append(i.file.summary)
        userid.append(str(i.user.id))
        username.append(i.user.name)
    return jsonify(get_dict(dic_comm_ok, {
        'total': total, 'fidlist': str(fidlist),
        'namelist': namelist, 'datelist': datelist,
        'classifylist': classifylist, 'summarylist': summarylist, 'userid': userid,
        'username':username}))


