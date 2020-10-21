# -*- coding = utf-8 -*-
# @Time : 2020/10/5 10:29
# @Author : Chenih
# @File : __init__.py.py
# @Software : PyCharm
from flask import Flask

import settings
from apps.article.views import article_bp

from apps.user.views import user_bp1
from exts import db, bootstrap


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings.DevelopmentConfig)
    # 初始化db
    db.init_app(app=app)
    # 初始化bootstrap
    bootstrap.init_app(app=app)

    app.register_blueprint(user_bp1)
    app.register_blueprint(article_bp)

    return app
