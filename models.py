#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from exts import db
from datetime import datetime


# 自定义模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Ask(db.Model):
    __tablename__ = 'ask'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tittle = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # now()获取的是服务器第一次运行的时间
    #now是每次创建一个模型的时候，都会获取当前时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('asks'))


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    ask_id = db.Column(db.Integer, db.ForeignKey('ask.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Ask.create_time.desc()代表的是从大到小排序，去掉.desc()，默认从小到大排序
    # order_by=id.desc()代表的按照id从大到小排序，不写这个order_by参数，默认从小到大排序
    ask = db.relationship('Ask', backref=db.backref('answers', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))

