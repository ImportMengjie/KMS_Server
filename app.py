import base64
import hashlib
import io

import os
from mongoengine import NotUniqueError, ValidationError

from common import *
from model import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


@app.route('/', methods=['Get'])
def hello_world():
    return 'Hello World!'


@app.route('/app/see', methods=['Get'])
def see_hot():
    pass


@app.route('/app/register', methods=['Post'])
def register():
    u = User()
    u.set_phone(request.json.get('phone'))
    u.name = request.json.get('name')
    u.set_email(request.json.get('email'))
    u.hash_password(request.json.get('password'))
    u.list_favorite = ""
    if len(request.json.get('password')) < 6:
        return jsonify(dic_comm_format_error)
    try:
        u.save()
    except NotUniqueError as e:
        print(e)
        return jsonify(dic_register_has_been_register), HTTP_Forbidden
    except ValidationError as e:
        print(e)
        return jsonify(dic_comm_format_error), HTTP_Forbidden
    except BaseException as e:
        print(e)
        return jsonify(dic_comm_server_error), HTTP_Server_Error
    return jsonify(dic_register_success), HTTP_OK


@app.route('/app/register/testphone', methods=['Post'])
def test_phone():
    phone = request.json.get('phone')
    if not validate_phone(phone):
        return jsonify(dic_comm_format_error), HTTP_Forbidden
    if User.objects(phone=phone):
        return jsonify(dic_register_has_been_register), HTTP_Forbidden
    return jsonify(dic_register_isok_register)


@app.route('/app/login', methods=['Post'])
def login():
    phone = request.json.get('phone')
    password = request.json.get('password')
    if not phone or not password or len(password) < 6 or not validate_phone(phone):
        return jsonify(dic_comm_format_error), HTTP_Forbidden
    u = User.objects(phone=phone).first()
    if not u:
        return jsonify(dic_login_notfound), HTTP_Forbidden
    if not u.verify_password(password):
        return jsonify(dic_login_pw_erro), HTTP_Forbidden
    token = hashlib.sha1(os.urandom(24)).hexdigest()
    first_login = False if u.token else True
    u.token = token
    u.save()
    # dic_login_success.update()
    return jsonify(get_dict(dic_login_success, {'first_time': first_login, 'token': token})), HTTP_OK


@app.route('/app/user/avatar', methods=['Post'])
@auth_token
def upload_avatar(user):
    data = request.json.get('data')
    if not data:
        return jsonify(dic_comm_format_error), HTTP_Forbidden
    print(data)
    file = base64.b64decode(data)
    file_like = io.BytesIO(file)
    user.photo.replace(file_like)
    user.save()
    return jsonify(dic_avatar_ok), HTTP_OK


@app.route('/app/user/get_avatar', methods=['Get'])
@auth_token
def get_avatar(user):
    photo = user.photo.read()
    if photo:
        data = base64.b64encode(photo)
        # dic_avatar_ok.update()
        return jsonify(get_dict(dic_avatar_ok, {'data': str(data)})), HTTP_OK
    return jsonify(dic_comm_not_found), HTTP_NotFound


@app.route('/app/user/upload', methods=['Post'])
@auth_token
def upload(user):
    name = request.json.get('name')
    data = request.json.get('data')
    public = request.json.get('public')
    md5 = request.json.get('md5')
    if md5 and name and public:
        file_field = File.objects(md5=md5).first()
        if file_field:
            user_file = UserFile(name=name, date=datetime.now(), public=public)
            user_file.user = user
            user_file.file = file_field
            file_field.sum_point += 1
            user_file.classify = UserFile.objects(file=file_field).first().classify
            user_file.user_classify = user_file.classify.name
            user_file.save()
            return jsonify(get_dict(dic_upload_create_ok, {'fid': str(user_file.id, 'utf-8'),
                                                           'summary': file_field.summary,
                                                           'classify': user_file.classify.name})), HTTP_OK
        else:
            return jsonify(dic_comm_not_found), HTTP_NotFound
    if name and data and public:
        user_file = UserFile(name=name, date=datetime.now(), public=public)
        file = base64.b64decode(data)
        md5 = hashlib.md5()
        md5.update(file)
        md5 = md5.hexdigest()
        file_field = File.objects(md5=md5).first()
        if file_field:
            file_field.sum_point += 1
            file_field.save()
            user_file.user = user
            user_file.file = file_field
            user_file.classify = UserFile.objects(file=file_field).first().classify
            user_file.user_classify = user_file.classify.name
            user_file.save()
            return jsonify(get_dict(dic_upload_create_ok, {'fid': str(user_file.id),
                                                           'summary': file_field.summary,
                                                           'classify': user_file.classify.name})), HTTP_OK
        else:
            file_field = File(upload_user=user, md5=md5, upload_date=datetime.now())
            try:
                text = handle_file(file)
                summary = handle_summary(file)
                classify = handle_classify(file, summary, text)
            except TypeError as e:
                return jsonify(dic_comm_format_error), HTTP_Bad_Request
            file_field.summary = summary
            file_field.text = text
            file_like = io.BytesIO(file)
            file_field.file.put(file_like)
            file_field.save()
            user_file.user = user
            user_file.file = file_field
            user_file.classify = classify
            user_file.user_classify = user_file.classify.name
            user_file.save()
            return jsonify(get_dict(dic_upload_ok, {'fid': str(user_file.id),
                                                    'summary': file_field.summary,
                                                    'classify': user_file.classify.name})), HTTP_OK
    else:
        return jsonify(dic_comm_format_error), HTTP_Forbidden


@app.route('/app/user/getfile', methods=['Get'])
@auth_token
def getfile(user):
    fid = request.json.get('fid')
    user_file = UserFile.objects(id=fid).first()
    if user_file:
        file = user_file.file.file.read()
        if file:
            data = base64.b64encode(file)
            return jsonify(get_dict(dic_file_get_ok, {'data': str(data), 'date': user_file.date,
                                                      'classify': user_file.user_classify,
                                                      'summary': user_file.file.summary})), HTTP_OK
        else:
            return jsonify(dic_comm_not_found), HTTP_NotFound
    else:
        return jsonify(dic_comm_not_found), HTTP_NotFound


@app.route('/app/user/modifyfile', methods=['Post'])
@auth_token
def modifyfile(user):
    fid = request.json.get('fid')
    public = request.json.get('public')
    name = request.json.get('name')
    classify = request.json.get('classify')
    delete = request.json.get('delete')
    if fid:
        user_file = UserFile.objects(id=fid).first()
        if not user_file:
            return jsonify(dic_comm_not_found), HTTP_NotFound
        if delete:
            user_file.file.sum_point -= 1
            if user_file.file.sum_point == 0:
                user_file.file.delete()
                user_file.delete()
            else:
                user_file.file.save()
                user_file.delete()
            return jsonify(dic_file_dele_ok), HTTP_OK
        if public or name or classify:
            user_file.name = name if name else user_file.name
            user_file.public = public if public is not None else user_file.public
            user_file.user_classify = classify if classify else user_file.user_classify
            user_file.save()
            return jsonify(dic_file_modify_ok), HTTP_OK
        else:
            return jsonify(dic_file_modify_none), HTTP_OK

    else:
        return jsonify(dic_comm_format_error), HTTP_Forbidden


@app.route('/app/user/modify', methods=['POST'])
@auth_token
def user_modify(user):
    name = request.json.get('name')
    birth = request.json.get('birth')
    password = request.json.get('password')
    if not password and not name and not birth:
        return jsonify(dic_modify_none), HTTP_Forbidden
    user.name = name if name else user.name
    user.birth = birth if birth else user.birth
    user.hash_password(password)
    try:
        user.save()
    except ValidationError as e:
        print(e)
        return jsonify(dic_comm_format_error), HTTP_Forbidden
    except BaseException as e:
        print(e)
        return jsonify(dic_comm_server_error), HTTP_Server_Error
    return jsonify(dic_modify_ok), HTTP_OK


@app.route('/app/user/info', methods=['POST'])
@auth_token
def user_info(user):
    userid = request.json.get('userid')
    if not userid:
        return jsonify(
            get_dict(dic_comm_ok, {'name': user.name, 'phone': user.phone,
                                   'email': user.email, 'birth': user.birth})), HTTP_OK
    else:
        user = User(id=userid).first()
        if user:
            return jsonify(
                get_dict(dic_comm_ok, {'name': user.name, 'phone': user.phone,
                                       'email': user.email, 'birth': user.birth})), HTTP_OK
        else:
            return jsonify(dic_comm_not_found), HTTP_NotFound


@app.route('/app/user/getownfilelist', methods=['Get'])
@auth_token
def get_ownfilelist(user):
    res = UserFile.objects(user=user, isfavorite=False)
    total = len(res)
    fidlist = []
    namelist = []
    datelist = []
    classifylist = []
    summarylist = []
    public = []
    for i in res:
        fidlist.append(i.id)
        namelist.append(i.name)
        datelist.append(i.date)
        classifylist.append(i.user_classify)
        summarylist.append(i.file.summary)
        public.append(i.public)
    return jsonify(get_dict(dic_comm_ok, {
        'total': total, 'fidlist': str(fidlist),
        'namelist': namelist, 'datelist': datelist,
        'classifylist': classifylist, 'summarylist': summarylist, 'public': public}))


@app.route('/app/user/getfilelist', methods=['Get'])  # 获取推荐列表
@auth_token
def getfilelist(user):
    pass


@app.route('/app/user/favorite', methods=['Post'])
@auth_token
def favorite(user):
    fid = request.json.get('fid')
    cancel = request.json.get('cancel')
    if not fid and not cancel:
        res = UserFile.objects(user=user, isfavorite=True)
        total = len(res)
        fidlist = []
        namelist = []
        datelist = []
        classifylist = []
        summarylist = []
        public = []
        for i in res:
            fidlist.append(i.id)
            namelist.append(i.name)
            datelist.append(i.date)
            classifylist.append(i.user_classify)
            summarylist.append(i.file.summary)
            public.append(i.public)
        return jsonify(get_dict(dic_comm_ok, {
            'total': total, 'fidlist': str(fidlist),
            'namelist': namelist, 'datelist': datelist,
            'classifylist': classifylist, 'summarylist': summarylist, 'public': public}))
    elif fid and not cancel:
        user_file = UserFile.objects(id=fid).first()
        if not user_file:
            return jsonify(dic_comm_not_found), HTTP_NotFound
        elif user_file.user == user:
            return jsonify(dic_favorite_has_been), HTTP_Forbidden
        else:
            new_user_file = UserFile(name=user_file.name, date=user_file.date,
                                     file=user_file.file, user_classify=user_file.classify.name,
                                     user=user, public=True,
                                     classify=user_file.classify,isfavorite=True)
            new_user_file.file.sum_point += 1
            new_user_file.save()
            return jsonify(dic_favorite_ok),HTTP_OK
    elif fid and cancel:
        user_file=UserFile.objects(id=fid,user=user,isfavorite=True)
        if not user_file.first():
            return jsonify(dic_favorite_it_not_your),HTTP_Forbidden
        else:
            user_file = user_file.first()
            user_file.file.sum_point -= 1
            if user_file.file.sum_point == 0:
                user_file.file.delete()
                user_file.delete()
            else:
                user_file.file.save()
                user_file.delete()
                return jsonify(dic_favorite_cancel),HTTP_OK
    else:
        return jsonify(dic_comm_format_error),HTTP_Forbidden


# @app.route('/app/user/favorite', methods=['Post'])
# @auth_token
# def favorite(user):
#     fid = request.json.get('fid')
#     cancel = request.json.get('cancel')
#     if not fid and not cancel:
#         total = len(user.list_favorite)
#         fidlist = []
#         namelist = []
#         datelist = []
#         classifylist = []
#         summarylist = []
#         public = []
#         for s in user.list_favorite.split(','):
#             if s=="":
#                 continue
#             i = UserFile.objects(id=s).first()
#             fidlist.append(i.id)
#             namelist.append(i.name)
#             datelist.append(i.date)
#             classifylist.append(i.user_classify)
#             summarylist.append(i.file.summary)
#             public.append(i.public)
#         return jsonify(get_dict(dic_comm_ok, {
#             'total': total, 'fidlist': str(fidlist),
#             'namelist': namelist, 'datelist': datelist,
#             'classifylist': classifylist, 'summarylist': summarylist, 'public': public}))
#     if fid and not cancel:
#         user_file = UserFile.objects(id=fid).first()
#         if user.list_favorite.find(fid) >= 0 or user_file.user == user:
#             return jsonify(dic_favorite_has_been), HTTP_Forbidden
#         else:
#             user.list_favorite += ',' + fid
#             user.save()
#             return jsonify(dic_favorite_ok), HTTP_OK
#     elif fid and cancel:
#         index = user.list_favorite.find(fid)
#         if index < 0:
#             return jsonify(dic_favorite_it_not_your), HTTP_NotFound
#         else:
#             user.list_favorite = user.list_favorite.replace(','+fid, "")
#             user.save()
#             return jsonify(dic_favorite_cancel),HTTP_OK



if __name__ == '__main__':
    # app.run(debug=True, host='10.206.11.197')
    app.run(debug=True)
