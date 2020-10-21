# -*- coding = utf-8 -*-
# @Time : 2020/10/18 13:38
# @Author : Chenih
# @File : util.py
# @Software : PyCharm
import os
import random

from flask import session
from qiniu import Auth, put_file, etag, put_data, BucketManager
import qiniu.config
# 需要填写你的 Access Key 和 Secret Key
from apps.article.models import Article_type
from apps.user.models import User
from settings import Config

def upload_qiniu(filestorage):
    access_key = 'Y2epBqeCBXUkG6_Li_8fkpL2PgqQ6RuPFx74N-Ei'
    secret_key = 'miw2OtJI3-K-7q7LtpDWr3xnCOcPfp7dfzDhuWor'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间

    bucket_name = 'chenihphoto'
    # 上传后保存的文件名
    filename = filestorage.filename
    rnum = random.randint(1, 1000)
    suffix = filename.rsplit('.')[-1]
    key = filename.rsplit('.')[0] + '_' + str(rnum) + '.' + suffix
    # key = 'my-python-logo.png'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    # localfile = os.path.join(Config.UPLOAD_ICON_DIR, 'hdr.jpg')
    # ret, info = put_file(token, key, localfile)
    # print(info)
    # print(ret)
    ret, info = put_data(token, key, filestorage.read())
    return ret, info
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)

def del_qiqiu(filename):
    access_key = 'Y2epBqeCBXUkG6_Li_8fkpL2PgqQ6RuPFx74N-Ei'
    secret_key = 'miw2OtJI3-K-7q7LtpDWr3xnCOcPfp7dfzDhuWor'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'chenihphoto'
    # 初始化BucketManager(q)
    bucket = BucketManager(q)
    key = filename  # key就是文件名
    ret, info = bucket.delete(bucket_name, key)
    return info

def user_type():
    # 获取文章分类
    types = Article_type.query.all()
    # 登录用户
    user = None
    user_id = session.get('loginid', None)
    if user_id:
        user = User.query.get(user_id)
    return user, types
