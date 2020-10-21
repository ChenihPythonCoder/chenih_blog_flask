# -*- coding = utf-8 -*-
# @Time : 2020/10/10 12:23
# @Author : Chenih
# @File : views.py
# @Software : PyCharm
import os
from io import BytesIO

from dominate.svg import image
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, g

# url_prefix='/user'  以/user作为前导
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from apps.article.models import Article_type, Article
from apps.user.models import User, Photo, AboutMe, MssageBoard
from apps.user.smssend import SmsSendAPIDemo
from apps.utils.util import upload_qiniu, del_qiqiu
from exts import db
from settings import Config

user_bp1 = Blueprint('user', __name__, url_prefix='/user')

# 登录验证
required_login_list = ['/user/center', '/user/update', '/article/publish', '/user/upload_photo', '/user/myphoto', '/user/photo_del'
                       , '/article/add.comment', '/user/aboutme', '/user/board']
@user_bp1.before_app_request
def before_request():
    if request.path in required_login_list:
        loginid = session.get('loginid')
        if not loginid:
            return render_template('user/login.html')
        else:
            user = User.query.get(loginid)
            # g对象，本次请求的对象
            g.user = user

# 自定义过滤器
@user_bp1.app_template_filter('cdecode')
def content_decode(content):
    content = content.decode('utf-8')
    return content[:200]

@user_bp1.app_template_filter('edecode')
def content_decode(content):
    content = content.decode('utf-8')
    return content

@user_bp1.route('/')
def index():
    # cookie获取方式
    # loginid = request.cookies.get('loginid', None)
    # session获取方式, session底层默认获取
    loginid = session.get('loginid')
    # 接收页码数
    page = int(request.args.get('page', 1))
    # 获取文章列表
    pagination = Article.query.order_by(-Article.pdatetime).paginate(page=page, per_page=3)
    pagination.items
    # 获取分类列表
    types = Article_type.query.all()
    if loginid:
        user = User.query.get(loginid)
        return render_template('user/index.html', user=user, pagination=pagination, types=types)
    else:
        return render_template('user/index.html', pagination=pagination, types=types)

@user_bp1.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if password == repassword:
            user = User()
            user.username = username
            # 使用自带的函数实现加密：generate_password_hash
            user.password = generate_password_hash(password)
            user.phone = phone
            user.email = email
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.index'))
    return render_template('user/register.html')

@user_bp1.route('/checkphone')
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    # code:400 不能用   200 可以用
    if len(user) > 0:
        return jsonify(code=400, msg='号码已被注册')
    else:
        return jsonify(code=200, msg='号码可用')

@user_bp1.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        f = request.args.get('f')
        if f == '1':
            username = request.form.get('username')
            password = request.form.get('password')
            users = User.query.filter(User.username == username).all()
            for user in users:
                # check_password_hash返回值是布尔类型
                flag = check_password_hash(user.password, password)
                if flag:
                    # 1.cookie实现会话机制
                    # response = redirect(url_for('user.index'))
                    # response.set_cookie('loginid', str(user.id), max_age=3600)
                    # return response
                    # 2.session实现会话机制,session当成字典
                    session['loginid'] = user.id
                    return redirect(url_for('user.index'))
            else:
                return render_template('user/login.html', msg='用户名或密码有误！')
        elif f == '2':   # 手机号码验证码登录
            phone = request.form.get('phone')
            code = request.form.get('code')
            valid_code = session.get(phone)
            if code == valid_code:
                user = User.query.filter(User.phone==phone).first()
                if user:
                    session['loginid'] = user.id
                    return redirect(url_for('user.index'))
                else:
                    return render_template('user/login.html', msg='此号码未注册')
            else:
                return render_template('user/login.html', msg='验证码有误')


    return render_template('user/login.html')

@user_bp1.route('/sendMsg')
def send_message():
    phone = request.args.get('phone')
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "bdf011d120174ea393b036c225a37057"  # 业务ID，易盾根据产品业务特点分配
    api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
    params = {
        "mobile": phone,
        "templateId": "10084",
        "paramType": "json",
        "params": "json格式字符串"
    }
    ret = api.send(params)
    print(ret)
    session[phone] = '189075'
    return jsonify(code=200, msg='短信发送成功！')
    # if ret is not None:
    #     if ret["code"] == 200:
    #         taskId = ret["data"]["taskId"]
    #         print("taskId = %s" % taskId)
    #         session[phone] = '189075'
    #         return jsonify(code=200, msg='短信发送成功！')
    #     else:
    #         print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
    #         return jsonify(code=400, msg='发送失败！')


@user_bp1.route('/logout')
def logout():
    #1.cookie方式
    #response = redirect(url_for('user.index'))
    # 删除cookie
    #response.delete_cookie('loginid')
    # 2.删除session中的某一对key：value
    # del session['loginid']
    # 直接清除session空间
    session.clear()
    return redirect(url_for('user.index'))

# 用户中心
@user_bp1.route('/center')
def user_center():
    types = Article_type.query.all()
    photos = Photo.query.filter(Photo.user_id == g.user.id).all()

    return render_template('user/center.html', user=g.user, types=types, photos=photos)

# 发表文章
@user_bp1.route('/publish')
def publish_article():
    return render_template('user/publish')

# 上传照片
@user_bp1.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    photo = request.files.get('photo')
    # 将图片上传到云存储
    ret, info = upload_qiniu(photo)
    if info.status_code == 200:
        photo = Photo()
        photo.photo_name = ret['key']
        photo.user_id = g.user.id
        db.session.add(photo)
        db.session.commit()
        return '上传成功'
    else:
        return '上传失败'


# 可以上传的图片的扩展名
ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif', 'bmp']
# 修改用户信息
@user_bp1.route('/update', methods=['GET', 'POST'])
def userinfo_update():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        # 只要有文件（图片），获取方式必须使用request.files.get(name)
        icon = request.files.get('icon')
        # print('======>', icon)  # FileStorage
        # 属性： filename 用户获取文件的名字
        # 方法:  save(保存路径)
        icon_name = icon.filename  # 1440w.jpg
        suffix = icon_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            icon_name = secure_filename(icon_name)  # 保证文件名是符合python的命名规则
            file_path = os.path.join(Config.UPLOAD_ICON_DIR, icon_name)
            icon.save(file_path)
            # 保存成功
            user = g.user
            user.username = username
            user.phone = phone
            user.email = email
            path = 'upload/icon'
            user.icon = os.path.join(path, icon_name)
            db.session.commit()
            return redirect(url_for('user.user_center'))
        else:
            return render_template('user/center.html', user=g.user, msg='必须是扩展名是：jpg,png,gif,bmp格式')

    return render_template('user/center.html', user=g.user)

# 我的相册
@user_bp1.route('/myphoto')
def myphoto():
    # 分页
    page = int(request.args.get('page', 1))
    # photos是一个pagination类型
    photos = Photo.query.paginate(page=page, per_page=3)
    # 查询是否登录状态
    loginid = session['loginid']
    user = None
    if loginid:
        user = User.query.get(loginid)
    return render_template('user/myphoto.html', photos=photos, user=user)

# 删除照片
@user_bp1.route('/photo_del')
def photo_del():
    pid = request.args.get('pid')
    photo = Photo.query.get(pid)
    filename = photo.photo_name
    # 封装好的删除文件的函数
    info = del_qiqiu(filename)
    # 判断状态码
    if info.status_code == 200:
        # 删除数据库的内容
        db.session.delete(photo)
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:

        return render_template('500.html', err_msg='删除照片失败啦')


# 用户添加关于我的
@user_bp1.route('/aboutme', methods=['GET', 'POST'])
def aboutme():
    content = request.form.get('aboutme')
    try:
        aboutme = AboutMe()
        aboutme.content = content.encode('utf-8')
        # 必须是登陆状态，所以可以使用g取到用户id
        aboutme.user_id = g.user.id
        db.session.add(aboutme)
        db.session.commit()
    except Exception as err:
        return redirect(url_for('user.user_center'))
    else:
        return render_template('user/aboutme.html', user=g.user)

# 关于我的
@user_bp1.route('/showaboutme')
def show_aboutme():
    loginid = session.get('loginid')
    user = User.query.get(loginid)
    if user:
        return render_template('user/aboutme.html', user=user)
    else:
        msg = '您还处于未登录状态！'
        return render_template('user/aboutme.html', msg=msg)

# 留言板
@user_bp1.route('/board', methods=['GET', 'POST'])
def show_board():
    user = None
    uid = session.get('loginid', None)
    if uid:
        user = User.query.get(uid)
    # boards = MssageBoard.query.all()
    page = int(request.args.get('page', 1))
    boards = MssageBoard.query.order_by(-MssageBoard.mdatetime).paginate(page=page, per_page=10)

    if request.method == 'POST':
        content = request.form.get('board')
        msg_board = MssageBoard()
        msg_board.content = content
        if uid:
            msg_board.user_id = uid
        db.session.add(msg_board)
        db.session.commit()
        return redirect(url_for('user.show_board'))
    return render_template('user/msg_board.html', user=user, boards=boards)

# 删除留言
@user_bp1.route('/board_del')
def delete_board():
    bid = request.args.get('bid')
    if bid:
        msg_board = MssageBoard.query.get(bid)
        db.session.delete(msg_board)
        db.session.commit()
        return redirect(url_for('user.user_center'))