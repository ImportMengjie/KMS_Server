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
        return jsonify(dic_register_has_been_register), 403
    except ValidationError as e:
        print(e)
        return jsonify(dic_comm_format_error), 403
    except BaseException as e:
        print(e)
        return jsonify(dic_comm_server_error), 500
    return jsonify(dic_register_success), 201


@app.route('/app/register/testphone', methods=['Post'])
def test_phone():
    phone = request.json.get('phone')
    if not validate_phone(phone):
        return jsonify(dic_comm_format_error), 403
    if User.objects(phone=phone):
        return jsonify(dic_register_has_been_register), 403
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
    return jsonify(dic_login_success.update({'first_time':first_login}))


@app.route('/app/user/avatar', methods=['Post'])
@auth_token
def upload_avatar(user):
    data = request.json.get('data')
    if not data:
        return jsonify(dic_comm_format_error)
    print(data)
    file = base64.b64decode(data)
    file_like = io.BytesIO(file)
    user.photo.replace(file_like)
    user.save()
    return jsonify(dic_avatar_ok)


@app.route('/app/user/get_avatar', methods=['Post'])
@auth_token
def get_avatar(user):
    photo = user.photo.read()
    if photo:
        data = base64.b64encode(photo)
        return jsonify({json_success: True, 'data': str(data)}), 200
    return jsonify({json_success: False, 'msg': msg_file_notfound}), 404


@app.route('/app/user/upload', methods=['Post'])
@auth_token
def upload(user):
    name = request.json.get('name')
    data = request.json.get('data')
    type = request.json.get('type')
    md5 = request.json.get('md5')
    if md5 and name:
        file_field = File.objects(md5=md5).first()
        if file_field:
            user_file = UserFile(name=name, date=datetime.now())
            user_file.file = file_field
            file_field.sum_point += 1
            user_file.save()
            return jsonify({json_success: True, json_msg: msg_file_upload_ok, 'fid': user_file.id})
        else:
            return jsonify({json_success: False, json_msg: msg_file_notfound})
    if name and data and type:
        user_file = UserFile(name=name, date=datetime.now())
        file = base64.b64decode(data)
        md5 = hashlib.md5()
        md5.update(file)
        md5 = md5.hexhashlib()
        file_field = File.objects(md5=md5).first()
        if file_field:
            file_field.sum_point += 1
            file_field.save()
            user_file.file = file_field
            user_file.save()
            return jsonify({json_success: True, json_msg: msg_file_upload_ok, 'fid': user_file.id})
        else:
            file_field = File(upload_user=user, md5=md5, upload_date=datetime.now(), type=type)
            file_like = io.BytesIO(file)
            file_field.file.put(file_like)
            file_field.save()
            user_file.file = file_field
            user_file.save()
            return jsonify({json_success: True, json_msg: msg_file_upload_ok, 'fid': user_file.id})
    else:
        return jsonify({json_success: False, json_msg: msg_format_error})


@app.route('/app/user/getfile', methods=['Post'])
@auth_token
def getfile(user):
    fid = request.json.get('fid')
    file = UserFile.objects(id=fid).first()
    if file:
        file = file.file.file.read()
        if file:
            data = base64.b64encode(file)
            return jsonify({json_success: True, 'data': str(data)}), 200
        else:
            return jsonify({json_success: False, 'msg': msg_file_nodata}), HTTP_Forbidden
    else:
        return jsonify({json_success: False, 'msg': msg_file_notfound}), 404


@app.route('/app/user/modify', methods=['POST'])
@auth_token
def user_modify(user):
    name = request.json.get('name')
    birth = request.json.get('birth')
    password = request.json.get('password')
    if not password and not name and not birth:
        return jsonify({json_success: True, 'msg': 'no change'})
    user.name = name if name else user.name
    user.birth = birth if birth else user.birth
    user.hash_password(password)
    try:
        user.save()
    except ValidationError as e:
        print(e)
        return jsonify({json_success: False, 'msg': msg_format_error}), 403
    except BaseException as e:
        print(e)
        return jsonify({json_success: False, 'msg': msg_server_error}), 500
    return jsonify({json_success: True, json_msg: msg_modify_success})


@app.route('/app/user/info', methods=['POST'])
@auth_token
def user_info(user):
    return jsonify(
        {json_success: True, 'name': user.name, 'phone': user.phone, 'email': user.email, 'birth': user.birth})


if __name__ == '__main__':
    # app.run(debug=True, host='10.206.11.197')
    app.run(debug=True)