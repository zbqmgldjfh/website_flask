from flask import Flask
from flask import request
from flask import render_template
from flask_pymongo import PyMongo
from datetime import datetime
from datetime import timedelta
from bson.objectid import ObjectId
from flask import abort, redirect, url_for, flash, session
import time
import math

app = Flask(__name__)  #flask 인스턴스 생성
app.config["MONGO_URI"] = "mongodb://localhost:27017/myweb"
app.config["SECRET_KEY"] = "7a5bc45d"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30) # 세션유지시간 30분
mongo = PyMongo(app)

from .common import login_required
from .filter import format_datetime
from . import board
from . import member

app.register_blueprint(board.blueprint)
app.register_blueprint(member.blueprint)