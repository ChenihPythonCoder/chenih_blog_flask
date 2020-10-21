# -*- coding = utf-8 -*-
# @Time : 2020/10/4 15:58
# @Author : Chenih
# @File : settings.py
# @Software : PyCharm
import os


class Config():
    DEBUG = True
    # 什么数据库mysql + 驱动pymysql://user:password@hostip:port/databasename
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:020814@127.0.0.1:3306/flaskblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # secret_key
    SECRET_KEY = 'gsd999gsd888gsd'
    # 项目路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 静态文件夹的路径
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    # 头像的上传目录
    UPLOAD_ICON_DIR = os.path.join(STATIC_DIR, 'upload/icon')
    # 相册的上传目录
    UPLOAD_PHOTO_DIR = os.path.join(STATIC_DIR, 'upload/photo')


class DevelopmentConfig(Config):
    ENV = 'development'

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False

if __name__ == '__main__':
    print(Config.BASE_DIR)
    # print(os.path.abspath(__file__))
    print(Config.STATIC_DIR)
    print(Config.UPLOAD_ICON_DIR)