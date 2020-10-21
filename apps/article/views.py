# -*- coding = utf-8 -*-
# @Time : 2020/10/14 14:08
# @Author : Chenih
# @File : views.py
# @Software : PyCharm
from flask import Blueprint, request, render_template, g, redirect, url_for, jsonify, session

from apps.article.models import Article, Article_type, Comment
from apps.user.models import User
from apps.utils.util import user_type
from exts import db

article_bp = Blueprint('article', __name__, url_prefix='/article')

# 自定义过滤器
@article_bp.app_template_filter('ddecode')
def content_decode(content):
    content = content.decode('utf-8')
    return content


@article_bp.route('/publish', methods=['GET', 'POST'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        type_id = request.form.get('type')
        content = request.form.get('content')
        article = Article()
        article.title = title
        article.type_id = type_id
        article.content = content
        article.user_id = g.user.id
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('user.index'))


@article_bp.route('/detail')
def article_detail():
    article_id = request.args.get('aid')
    article = Article.query.get(article_id)
    types = Article_type.query.all()
    user = None
    user_id = session.get('loginid', None)
    if user_id:
        user = User.query.get(user_id)
    # 单独查询评论
    page = int(request.args.get('page', 1))
    comments = Comment.query.filter(Comment.article_id == article_id)\
        .order_by(-Comment.cdatetime)\
        .paginate(page=page, per_page=5)
    return render_template('article/detail.html', article=article, types=types, user=user, comments=comments)

@article_bp.route('/love')
def article_love():
    article_id = request.args.get('aid')
    tag = request.args.get('tag')

    article = Article.query.get(article_id)
    if tag == '1':
        article.love_num -= 1
    else:
        article.love_num += 1
    db.session.commit()
    return jsonify(num=article.love_num)

@article_bp.route('/save')
def article_save():
    article_id = request.args.get('aid')
    tag = request.args.get('tag')

    article = Article.query.get(article_id)
    if tag == '1':
        article.save_num -= 1
    else:
        article.save_num += 1
    db.session.commit()
    return jsonify(num=article.save_num)

@article_bp.route('/add.comment', methods=['GET', 'POST'])
def article_comment():
    if request.method == 'POST':
        content = request.form.get('content')
        user_id = g.user.id
        article_id = request.form.get('article_id')
        comment = Comment()
        comment.user_id = user_id
        comment.comment = content
        comment.article_id = article_id
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article.article_detail') + '?aid=' + article_id)
    return redirect(url_for('user.index'))

# 文章分类检索
@article_bp.route('/type_search')
def type_search():

    user, types = user_type()


    # 类型id的获取
    tid = request.args.get('tid', 1)
    page = int(request.args.get('page', 1))

    #分页

    articles = Article.query.filter(Article.type_id == tid).paginate(page=page, per_page=10)

    params = {
        'user': user,
        'types': types,
        'articles': articles,
        'tid': tid
    }

    return render_template('article/article_type.html', **params)