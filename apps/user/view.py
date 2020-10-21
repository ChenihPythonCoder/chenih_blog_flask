# -*- coding = utf-8 -*-
# @Time : 2020/10/5 10:36
# @Author : Chenih
# @File : view.py
# @Software : PyCharm
import hashlib

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import or_

from apps.user.models import User
from exts import db

user_bp = Blueprint('user', __name__)

# 注册
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        if password == repassword:
            # 注册用户
            user = User()
            user.username = username
            user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            user.phone = phone
            # 添加并提交
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.user_center'))
    return render_template('user/register.html')
# 信息中心
@user_bp.route('/')
def user_center():
    # 查询数据库中的数据
    users = User.query.filter(User.isdelete==False).all()  # select * from table;
    return render_template('user/center.html', users=users)

# 登录
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        shapassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # 查询
        user_list = User.query.filter_by(username=username)
        for user in user_list:
            if user.password == shapassword:
                return '用户登陆成功！'
        else:
            return render_template('user/login.html', msg='用户名或密码错误！')

    return render_template('user/login.html')

# 检索
@user_bp.route('/search')
def search():
    keyword = request.args.get('search')
    # 查询
    user_list = User.query.filter(or_(User.username.contains(keyword), User.phone.contains(keyword))).all()
    return render_template('user/center.html', users=user_list)

# 删除
@user_bp.route('/delete')
def user_delete():
    # 获取用户id
    id = request.args.get('id')
    # # 获取该id的用户
    user = User.query.get(id)
    # # 1.逻辑删除
    # user.isdelete = True
    # db.session.commit()
    # 2.物理删除
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('user.center.html'))

@user_bp.route('/update', methods=['GET', 'POST'])
def user_update():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        id = request.form.get('id')
        # 找用户
        user = User.query.get(id)
        # 修改信息
        user.username = username
        user.phone = phone
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        id = request.args.get('id')
        user = User.query.get(id)
        return render_template('user/update.html', user=user)






# @user_bp.route('/select')
# def user_select():
#     user = User.query.get(2)  # 根据主键查询
