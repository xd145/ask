#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Ask, Answer
from exts import db
from decorators import login_required


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        # 查询ask模型所有数据，并倒序排列出来
        'asks': Ask.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone==telephone, User.password==password).first()
        if user:
            session['user_id'] = user.id
            # 如果想设置31天都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '手机号码或密码错误'


@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证，如果已经注册过了，就不能再次注册
        user = User.query.filter(User.telephone==telephone).first()
        if user:
            return '该手机号码已被注册，请直接登录'
        else:
            # 要password1与password2密码一样，才能通过验证
            if password1 != password2:
                return '输入的密码不一致，请重新填写'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 注册成功后，页面跳转到登录页面
                return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # 删除session保存的user_id即可
    # del session['user_id']
    # session.clear()
    session.pop('user_id')
    return redirect(url_for('login'))

@app.route('/ask/', methods=['GET','POST'])
@login_required
def ask():
    if request.method == 'GET':
        return render_template('ask.html')
    else:
        tittle = request.form.get('tittle')
        content = request.form.get('content')
        # 新增发布的数据
        ask = Ask(tittle=tittle, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        ask.author = user
        db.session.add(ask)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<detail_id>')
def detail(detail_id):
    ask_model = Ask.query.filter(Ask.id == detail_id).first()
    return render_template('detail.html', ask=ask_model)


#Answer
@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    ask_id = request.form.get('ask_id')

    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    ask = Ask.query.filter(Ask.id == ask_id).first()
    answer.ask = ask
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', detail_id=ask_id))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    user = User.query.filter(User.id==user_id).first()
    if user:
        return {'user':user}
    return {}


if __name__ == '__main__':
    app.run()
