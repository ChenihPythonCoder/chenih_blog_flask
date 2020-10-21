# -*- coding = utf-8 -*-
# @Time : 2020/10/15 20:53
# @Author : Chenih
# @File : test.py
# @Software : PyCharm
import os

from qiniu import Auth, put_file, etag
import qiniu.config
#需要填写你的 Access Key 和 Secret Key
from settings import Config

access_key = 'Y2epBqeCBXUkG6_Li_8fkpL2PgqQ6RuPFx74N-Ei'
secret_key = 'miw2OtJI3-K-7q7LtpDWr3xnCOcPfp7dfzDhuWor'
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'chenihphoto'
#上传后保存的文件名
key = 'my-python-logo.png'
#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)
#要上传文件的本地路径
localfile = os.path.join(Config.UPLOAD_ICON_DIR, 'hdr.jpg')
ret, info = put_file(token, key, localfile)
print(info)
print(ret)

# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)