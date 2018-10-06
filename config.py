#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pymysql

DEBUG = True

SECRET_KEY = os.urandom(24)

# 配置数据库地址地址
# 跟踪数据库的修改 --> 不建议开启，未来版本会移除
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql123@127.0.0.1:3306/ask'
SQLALCHEMY_TRACK_MODIFICATIONS = False




