# -*- coding: utf-8 -*-
"""
the model of authentication blueprint
"""
from utils.ext import db
from flask_security import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from utils.ext import login_manager
import base64


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    photo = db.Column(db.LargeBinary(length=2048))
    password_hash = db.Column(db.String(255))
    permission = db.Column(db.Integer)
    balance = db.Column(db.Float)
    verificationcode = db.Column(db.String(20))
    confirmed_at = db.Column(db.DateTime(), default=datetime.now())

    @property
    def password(self):

        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):

        return check_password_hash(self.password_hash, password)

    def to_json(self):

        doc = self.__dict__
        if '_sa_instance_state' in doc:
            del doc['_sa_instance_state']

        if "password_hash" in doc:
            del doc['password_hash']

        if "verificationcode" in doc:
            del doc['verificationcode']

        if doc.get('confirmed_at', None):
            doc['confirmed_at'] = doc['confirmed_at'].strftime('%F %T')

        if doc.get('photo', None):
            doc['photo'] = str(base64.b64encode(doc['photo']))

        return doc


class Answerer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    photo = db.Column(db.LargeBinary(length=2048))
    resume = db.Column(db.String(512))
    field = db.Column(db.Integer)  # 该项为下拉框可选项
    price = db.Column(db.Float)
    month_income = db.Column(db.String(255), default="0#0#0#0#0#0#0#0#0#0#0#0")
    year_income = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime(), default=datetime.now())

    def to_json(self):

        doc = self.__dict__
        if '_sa_instance_state' in doc:
            del doc['_sa_instance_state']

        if doc.get('confirmed_at', None):
            doc['confirmed_at'] = doc['confirmed_at'].strftime('%F %T')

        if doc.get('photo', None):
            doc['photo'] = str(base64.b64encode(doc['photo']))

        return doc
