import re
from io import BufferedReader

from flask_mongoengine import MongoEngine
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from config import *

db = MongoEngine()

class User(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(max_length=55)
    phone = db.StringField(max_length=11, min_length=11, unique=True,required=True)
    password = db.StringField(max_length=128, required=True)
    birth = db.DateTimeField()
    photo = db.ImageField(thumbnail_size=(60,60,True))
    token = db.StringField()
    def hash_password(self, password):
        if password:
            self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def set_email(self, email: str):
        if validate_email(email):
            self.email = email

    def set_phone(self, phone: str):
        if validate_phone(phone):
            self.phone = phone

class Classify(db.Document):
    name = db.StringField()
    id = db.LongField()

class File(db.Document):
    upload_user = db.ReferenceField(User)
    md5 = db.StringField()
    sum_point = db.LongField(default=1)
    upload_date = db.DateTimeField()
    file = db.FileField()


class UserFile(db.Document):
    name = db.StringField()
    date = db.DateTimeField()
    file = db.ReferenceField(File)
    classify = db.ReferenceField(Classify)
    user = db.ReferenceField(User)





# class FileDocument(db.Document):
#     meta = {
#         'allow_inheritance': True,
#     }
#     upload_user = db.ReferenceField(User)
#     md5 = db.StringField()
#     sum_point = db.LongField()
#     upload_date = db.DateTimeField()
#
# class File(db.Document):
#     meta = {
#         'allow_inheritance': True,
#     }
#     name = db.StringField()
#     date = db.DateTimeField()
#
#
# class VoiceFile(FileDocument):
#     file = db.BinaryField()
#
# class VideoFile(FileDocument):
#     file = db.FileField()
#
# class TextFile(FileDocument):
#     file = db.StringField()
#
# class RichTextFile(FileDocument):
#     file = db.FileField()
#
#
#
#
# class Voice(File):
#     file = db.ReferenceField(VoiceFile)
#
#
# class Video(File):
#     file = db.ReferenceField(VideoFile)
#
#
# class Text(File):
#     file = db.ReferenceField(TextFile)
#
# class RichText(File):
#     file = db.ReferenceField(RichTextFile)


def validate_phone(phone: str):
    if phone and len(phone)==11 and phone.isdigit() and phone[0] == '1':
        return True
    return False


def validate_email(email: str):
    if email and re.match('^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$', email):
        return True
    return False



if __name__ == '__main__':
    print(validate_email('limengjieqq.com'))
    a = BufferedReader()