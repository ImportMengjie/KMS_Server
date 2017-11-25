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
                summarry = handle_summary(file)
                classify = handle_classify(file, summarry, text)
            except TypeError as e:
                return jsonify(dic_comm_format_error), HTTP_Bad_Request
            file_field.summary = summarry
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
                                                      'classify':user_file.user_classify,
                                                      'summary':user_file.file.summary})), HTTP_OK
        else:
            return jsonify(dic_comm_not_found), HTTP_NotFound
    else:
        return jsonify(dic_comm_not_found), HTTP_NotFound


@app.route('/app/user/modifyfile', methods=['Post'])
@auth_token
def modifyfile(user):
    fid = request.json.get('fid')
    public=request.json.get('public')
    name=request.json.get('name')
    classify=request.json.get('classify')
    delete=request.json.get('delete')
    if fid:
        if delete:
            pass
        if public or name or classify:
            pass
    else:
        return jsonify(dic_comm_format_error),HTTP_Forbidden

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

    return jsonify(
        get_dict(dic_comm_ok, {'name': user.name, 'phone': user.phone,
                               'email': user.email, 'birth': user.birth})), HTTP_OK




@app.route('/app/user/getownfilelist', methods=['Get'])
@auth_token
def get_ownfilelist(user):
    res = UserFile.objects(user=user)


if __name__ == '__main__':
    # app.run(debug=True, host='10.206.11.197')
    app.run(debug=True)
