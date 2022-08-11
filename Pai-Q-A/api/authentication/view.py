# -*- coding: utf-8 -*-
"""
the view of authentication
"""
from flask_restful import Resource, reqparse
from .model import User, Answerer
import logging
from utils.errorCode import *
from utils.ext import db
from utils.imTool import TLSSigAPIv2
from werkzeug.security import generate_password_hash
from werkzeug.datastructures import FileStorage
from utils.task import send_async_email
import base64
from datetime import datetime
import random
import string


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, location='form')
        self.parser.add_argument('password', type=str, required=True, location='form')
        super(Login, self).__init__()

    def post(self):
        """
          login verification and send token
          ---
          tags:
            - Login
          parameters:
            - name: body
              in: body
              type: object
              required: true
              schema:
                id: login
                properties:
                  username:
                    type: string
                  password:
                    type: string

          responses:
            401:
              description: Login Verification Error!
            200:
              description: Successful Operation!
        """

        state = STATE_OK
        data = self.parser.parse_args()
        username = data.get("username", None)
        password = data.get("password", None)
        user = User.query.filter_by(username=username).first()
        if user is None or (not user.verify_password(password)):
            state = STATE_LOGIN_ERR
            return {'state': "Login Verification Error!"}, state.eid
        doc = user.to_json()
        return {'doc': doc, 'state': "Successful Operation!"}, state.eid


class Register(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, location='form')
        self.parser.add_argument('password', type=str, required=True, location='form')
        self.parser.add_argument('email', type=str, required=True, location='form')
        self.parser.add_argument('photo', type=FileStorage, required=True, location='files')
        super(Register, self).__init__()

    def get(self):
        return "just a test"

    def post(self):
        """
          for user to register
          ---
          tags:
            - Register
          parameters:
            - name: body
              in: body
              type: object
              required: true
              schema:
                id: register
                properties:
                  username:
                    type: string
                  password:
                    type: string
                  email:
                    type: string

          responses:
            403:
              description: Username or email already exits!
            201:
              description: Register Success!
        """
        data = self.parser.parse_args()
        username = data.get("username", None)
        password = data.get("password", None)
        email = data.get("email", None)
        photo = data['photo'].read()
        # if User.query.filter_by(username=username) is not None:
        if User.query.filter_by(username=username).count() > 0 or User.query.filter_by(email=email).count() > 0:
            logging.error("username or email already exits")
            state = STATE_REGISTER_ERR
            return {'state': "Username or email already exits!"}, state.eid
        user = User(username=username, email=email, permission=1, balance=0.0, photo=photo)
        user.set_password = password
        db.session.add(user)
        db.session.commit()
        state = STATE_CREATE_OK
        return {'state': "Register Success!"}, state.eid


class Upgrade(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, location='form')
        self.parser.add_argument('resume', type=str, required=True, location='form')
        self.parser.add_argument('field', type=int, required=True, location='form')
        self.parser.add_argument('price', type=float, required=True, location='form')
        super(Upgrade, self).__init__()

    def get(self):
        return "just a test"

    def post(self):
        """
          upgrade user to answer
          ---
          tags:
            - Upgrade
          parameters:
            - name: body
              in: body
              type: object
              required: true
              schema:
                id: upgrade
                properties:
                  username:
                    type: string
                  resume:
                    type: string
                  field:
                    type: integer
                  price:
                    type: float

          responses:
            402:
              description: User Not Exist!
            200:
              description: User Upgrade Success!
        """

        data = self.parser.parse_args()
        username = data.get("username", None)
        resume = data.get("resume", None)
        field = data.get("field", None)
        price = data.get("price", None)
        if price != price:
            return {'state': "please input integer or float!"}, 402
        user = User.query.filter_by(username=username).first()
        if user is None:
            logging.error("user does not exist")
            state = STATE_EmptyData_ERR
            return {'state': "User Not Exist!"}, state.eid
        elif Answerer.query.filter_by(username=username).first() is not None:
            db.session.query(Answerer).filter(Answerer.username == username).update({"resume": resume})
            db.session.query(Answerer).filter(Answerer.username == username).update({"field": field})
            db.session.query(Answerer).filter(Answerer.username == username).update({"price": price})
            db.session.commit()
            user.permission = 2
            return {'state': "User Upgrade Success!"}, 200
        else:
            answerer = Answerer(username=username, resume=resume, field=field, price=price, photo=user.photo)
            db.session.add(answerer)
            db.session.commit()
            state = STATE_CREATE_OK
            user.permission = 2
            return {'state': "User Upgrade Success!"}, 200


class SendAnsInfo(Resource):
    def __init__(self):
        super(SendAnsInfo, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)

    def get(self):
        """
          send the information array of all answerers
          ---
          tags:
            - SendAnsInfo

          responses:
            200:
              description: Successful Operation!
              schema:
                id: answerer
                properties:
                  id:
                    type: integer
                  username:
                    type: string
                  photo:
                    type: integer
                  resume:
                    type: string
                  field:
                    type: integer
                  price:
                    type: float
                  month_income:
                    type: string
                  year_income:
                    type: string
                  confirmed_at:
                    type: string
        """
        data = self.parser.parse_args()
        username = data.get("username", None)
        answerers = Answerer.query.all()
        res = []
        for answerer in answerers:
            if answerer.username != username:
                res.append(answerer.to_json())
        return {'res': res, 'state': "Successful Operation!"}, 200


class WalletManagement(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, location='form')
        self.parser.add_argument('money', type=float, required=False, location='form')
        super(WalletManagement, self).__init__()

    def get(self):
        """
          send the balance of some user
          ---
          tags:
            - WalletManagement
          parameters:
            - name: username
              in: path
              type: string
              required: true
              description: username

          responses:
            402:
              description: User Empty!
            200:
              description: Successful Operation!
              schema:
                id: balance
                properties:
                  balance:
                    type: float
        """

        data = self.parser.parse_args()
        username = data.get("username", None)
        user = User.query.filter_by(username=username).first()
        if user is None:
            logging.error("user does not exist")
            state = STATE_EmptyData_ERR
            return {'state': "User Empty!"}, state.eid
        else:
            balance = user.balance
            state = STATE_OK
            return {'balance': balance, 'state': "Successful Operation!"}, state.eid

    def post(self):
        """
          for user to recharge
          ---
          tags:
            - recharge
          parameters:
            - name: body
              in: body
              type: object
              required: true
              schema:
                id: recharge
                properties:
                  username:
                    type: string
                  money:
                    type: float

          responses:
            402:
              description: User Not Exist!
            200:
              description: Successful Operation!
        """

        data = self.parser.parse_args()
        username = data.get("username", None)
        money = data.get("money", None)
        user = User.query.filter_by(username=username).first()
        if user is None:
            logging.error("user does not exist")
            state = STATE_EmptyData_ERR
            return {'state': "User Not Exist!"}, state.eid
        user.balance += money
        state = STATE_OK
        return {'state': "Successful Operation!"}, 200


class genUserSig(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        super(genUserSig, self).__init__()

    def get(self):
        """
          return the sig of some user
          ---
          tags:
            - getUserSig
          parameters:
            - name: username
              in: path
              type: string
              required: true

          responses:
            200:
              description: Successful Operation!
              schema:
                id: sig
                properties:
                  sig:
                    type: string
        """

        data = self.parser.parse_args()
        username = data.get("username", None)
        api = TLSSigAPIv2(1400581926, 'bb2cf91db429a42442c6d1d81fe655b5f5e49a5ebd36454497b442b9958d2e5c')
        sig = api.genUserSig(username)

        return {'sig': sig, 'state': 'Successful Operation!'}, 200


class SendUserList(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        super(SendUserList, self).__init__()

    def get(self):
        """
          send the username list except of temporal user
          ---
          tags:
            - sendUserList
          parameters:
            - name: username
              in: path
              type: string
              required: true

          responses:
            200:
              description: Successful Operation!
              schema:
                id: user
                properties:
                  id:
                    type: integer
                  username:
                    type: string
                  email:
                    type: string
                  photo:
                    type: integer
                  password_hash:
                    type: string
                  permission:
                    type: integer
                  balance:
                    type: string
                  confirmed_at:
                    type: datetime
        """

        data = self.parser.parse_args()
        username = data.get("username", None)
        users = User.query.all()
        userList = []
        for user in users:
            if user.username != username:
                if User.query.filter_by(username=user.username).first().photo is None:
                    photo = ''
                else:
                    photo = str(base64.b64encode(User.query.filter_by(username=user.username).first().photo))
                user_dict = {'username': user.username, 'photo': photo}
                userList.append(user_dict)

        return {'userList': userList, 'state': 'Successful Operation!'}, 200


class AnswererInfo(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form')
        self.parser.add_argument('password', type=str, location='form')
        self.parser.add_argument('photo', type=FileStorage, location='files')
        self.parser.add_argument('email', type=str, location='form')
        self.parser.add_argument('price', type=str, location='form')
        self.parser.add_argument('field', type=str, location='form')
        self.parser.add_argument('resume', type=str, location='form')
        super(AnswererInfo, self).__init__()

    def post(self):
        """
              modify answer info
              ---
              tags:
                - answererinfo
              parameters:
                - name: body
                  in: body
                  type: object
                  required: true
                  schema:
                    properties:
                      username:
                        type: string
                      password:
                        type: string
                      photo:
                        type: file
                      email:
                        type: string
                      price:
                        type: string
                      field:
                        type: string
                      resume:
                        type: string

              responses:
                200:
                  description: Successful Operation!
                402:
                  description: Answerer do not exist!
            """
        data = self.parser.parse_args()
        username = data.get('username', None)
        answer = Answerer.query.filter_by(username=username).first()
        if answer is None:
            state = STATE_EmptyData_ERR
            return {'state': "Answer do not exist!"}, state.eid
        for key in data:
            if data.get(key) != '' and key != 'password':
                if key not in ('field', 'price', 'email', 'photo'):
                    db.session.query(Answerer).filter(Answerer.username == username).update({key: data.get(key)})
                    db.session.commit()
                elif key == 'field':
                    db.session.query(Answerer).filter(Answerer.username == username).update({key: int(data.get(key))})
                    db.session.commit()
                elif key == 'price':
                    db.session.query(Answerer).filter(Answerer.username == username).update({key: float(data.get(key))})
                    db.session.commit()
                elif key == 'email':
                    db.session.query(User).filter(User.username == username).update({key: data.get(key)})
                    db.session.commit()
                elif key == 'photo':
                    photo = data['photo'].read()
                    db.session.query(Answerer).filter(Answerer.username == username).update({'photo': photo})
                    db.session.commit()
            if data.get(key) != '' and key == 'password':
                password = data.get(key)
                password_hash = generate_password_hash(password=password)
                db.session.query(User).filter(User.username == username).update({'password_hash': password_hash})
                db.session.commit()

        state = STATE_OK
        return {'state': "Successful Operation!"}, state.eid


class ModifyUserInfo(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form')
        self.parser.add_argument('photo', type=FileStorage, location='files')
        self.parser.add_argument('email', type=str, location='form')
        super(ModifyUserInfo, self).__init__()

    def post(self):
        """
              modify user info
              ---
              tags:
                - userinfo
              parameters:
                - name: body
                  in: body
                  type: object
                  required: true
                  schema:
                    properties:
                      username:
                        type: string
                      photo:
                        type: file
                      email:
                        type: string

              responses:
                200:
                  description: Successful Operation!
                402:
                  description: User do not exist!
            """
        data = self.parser.parse_args()
        username = data.get('username', None)
        email = data.get("email", None)
        photo = data.get("photo", None)

        user = User.query.filter_by(username=username).first()
        if user is None:
            state = STATE_EmptyData_ERR
            return {'state': "User do not exist!"}, state.eid
        if email is not None:
            user.email = email
        if photo is not None:
            photo = photo.read()
            user.photo = photo
            answerer = Answerer.query.filter_by(username=username).first()
            if answerer is not None:
                answerer.photo = photo
        db.session.add(user)
        db.session.add(answerer)
        db.session.commit()
        state = STATE_OK
        return {'state': "Successful Operation!"}, state.eid


class ModifyPassword(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('originpassword', type=str)
        self.parser.add_argument('newpassword', type=str)
        super(ModifyPassword, self).__init__()

    def post(self):
        """
              modify password
              ---
              tags:
                - modifypassword
              parameters:
                - name: body
                  in: body
                  type: object
                  required: true
                  schema:
                    properties:
                      username:
                        type: string
                      originpassword:
                        type: string
                      newpassword:
                        type: string

              responses:
                200:
                  description: Successful Operation!
                400:
                  description: wrong password!
                402:
                  description: User do not exist!
            """
        data = self.parser.parse_args()
        username = data.get('username', None)
        originpassword = data.get('originpassword', None)
        newpassword = data.get('newpassword', None)
        user = User.query.filter_by(username=username).first()
        if user is None:
            state = STATE_EmptyData_ERR
            return {'state': "User do not exist!"}, state.eid
        if not user.verify_password(originpassword):
            state = STATE_PARAM_ERR
            return {'state': "wrong password!"}, state.eid
        new_password_hash = generate_password_hash(password=newpassword)
        db.session.query(User).filter(User.username == username).update({'password_hash': new_password_hash})
        db.session.commit()
        state = STATE_OK
        return {'state': "Successful Operation!"}, state.eid


class SendVerificationCode(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('email', type=str)
        super(SendVerificationCode, self).__init__()

    def post(self):
        """
              Send Verification Code
              ---
              tags:
                - SendVerificationCode
              parameters:
                - name: body
                  in: body
                  type: object
                  required: true
                  schema:
                    properties:
                      username:
                        type: string
                      email:
                        type: string

              responses:
                200:
                  description: Successful Operation!
                402:
                  description: User or email do not exist!
            """
        data = self.parser.parse_args()
        username = data.get('username', None)
        email = data.get('email', None)
        user = User.query.filter_by(username=username).first()
        if user is None or user.email != email:
            state = STATE_EmptyData_ERR
            return {'state': "User or email do not exist!"}, state.eid
        state = STATE_OK
        # generate verification code
        verification_code = ''
        for i in range(6):
            all_chars = string.ascii_letters + string.digits
            verification_code += random.choice(all_chars)
        email_data = {
            'subject': 'Send verification code',
            'to': email,
            'body': 'your verification code is ' + verification_code
        }
        user.verificationcode = verification_code
        db.session.commit()
        send_async_email.delay(email_data)
        return {'state': "successful operation!"}, state.eid


class FindPassword(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument("verificationcode", type=str)
        self.parser.add_argument('password', type=str)
        super(FindPassword, self).__init__()

    def post(self):
        """
              set new password
              ---
              tags:
                - FindPassword
              parameters:
                - name: body
                  in: body
                  type: object
                  required: true
                  schema:
                    properties:
                      username:
                        type: string
                      verificationcode:
                        type: string
                      password:
                        type: string

              responses:
                200:
                  description: Successful Operation!
                402:
                  description: verification code is wrong!
            """
        data = self.parser.parse_args()
        username = data.get('username', None)
        verificationcode = data.get("verificationcode", None)
        password = data.get("password", None)
        user = User.query.filter_by(username=username).first()
        if user is None or user.verificationcode != verificationcode:
            state = STATE_EmptyData_ERR
            return {'state': "User does not exist or verificationcode is wrong."}, state.eid
        state = STATE_OK
        # generate verification code
        new_password_hash = generate_password_hash(password=password)
        db.session.query(User).filter(User.username == username).update({'password_hash': new_password_hash})
        db.session.commit()
        return {'state': "successful operation!"}, state.eid

class GetUserMsg(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        super(GetUserMsg, self).__init__()

    def get(self):
        """
          return the Msg of some user
          ---
          tags:
            - GetUserMsg
          parameters:
            - name: username
              in: path
              type: string
              required: true

          responses:
            200:
              description: Successful Operation!
              schema:
                id: doc
                properties:
                  doc:
                    type: string
        """

        data = self.parser.parse_args()
        username = data.get("username", None)
        user = User.query.filter_by(username=username).first()
        if user is None:
            logging.error("user does not exist")
            state = STATE_EmptyData_ERR
            return {'state': "User Empty!"}, state.eid
        doc = user.to_json()
        return {'doc': doc, 'state': "Successful Operation!"}, 200


class SendAnsIncome(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        super(SendAnsIncome, self).__init__()

    def get(self):
        """
          send the income array of answerer
          ---
          tags:
            - SendAnsInfo

          responses:
            200:
              description: Successful Operation!
              schema:
                id: answerer
                properties:
                  month_income:
                    type: string
        """
        data = self.parser.parse_args()
        username = data.get("username", None)
        answerer = Answerer.query.filter_by(username=username).first()
        if answerer is None:
            state = STATE_EmptyData_ERR
            return {'state': "Income Verification Error!"}, state.eid
        return {'income': answerer.month_income, 'state': "Successful Operation!"}, 200


class ModifyAnsIncome(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form')
        self.parser.add_argument('income', type=float, location='form')
        super(ModifyAnsIncome, self).__init__()

    def post(self):
        """
          modify the income array of answerer
          ---
          tags:
            - ModifyAnsIncome

          responses:
            200:
              description: Successful Operation!
            402:
              description: User do not exist!
        """

        data = self.parser.parse_args()
        username = data.get("username", None)
        income = data.get("income", None)
        today = datetime.today()
        month = today.month

        answerer = Answerer.query.filter_by(username=username).first()
        if answerer is None:
            state = STATE_EmptyData_ERR
            return {'state': "Answerer do not exist!"}, state.eid
        income_str = answerer.month_income
        tmp = income_str.split('#')
        tmp[month - 1] = str(float(tmp[month - 1]) + income)
        answerer.month_income = '#'.join(tmp)
        return {'state': "Successful Operation!"}, 200
