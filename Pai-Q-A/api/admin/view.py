# -*- coding: utf-8 -*-
"""
the view of admin blueprint
"""
from flask_restful import Resource, reqparse
from .model import Admin, SystemConfigration
from utils.errorCode import *
from utils.ext import db
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
          upgrade user verification and send token
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
              schema:
                id: adminInfo
                properties:
                  username:
                    type: string
                  management:
                    type: integer
                  confirmed_at:
                    type: string
        """

        state = STATE_OK
        data = self.parser.parse_args()
        username = data.get("username", None)
        password = data.get("password", None)
        print("identified", username, password)
        admin = Admin.query.filter_by(username=username).first()
        if admin is None or (not admin.verify_password(password)):
            state = STATE_LOGIN_ERR
            return {'state': "Login Verification Error!"}, state.eid
        doc = admin.to_json()
        return {'info': doc, 'state': "Successful Operation!"}, state.eid


class AddAdmin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, location='form')
        super(AddAdmin, self).__init__()

    def post(self):
        """
          add admin and send password
          ---
          tags:
            - AddAdmin
          parameters:
            - name: body
              in: body
              type: object
              required: true
              schema:
                id: AddAdmin
                properties:
                  username:
                    type: string


          responses:
            403:
              description: username has already existed!
            200:
              description: Successful Operation!
              schema:
                id: Admin
                properties:
                  username:
                    type: string
                  password:
                    type: string
        """

        state = STATE_OK
        data = self.parser.parse_args()
        username = data.get("username", None)
        user = Admin.query.filter_by(username=username).first()
        if user is None:
            # permission 2 indicates that the user is normal admin
            admin = Admin(username=username, permission=2, management=0, confirmed_at=datetime.now())
            password = ''
            for i in range(10):
                all_chars = string.ascii_letters + string.digits
                password += random.choice(all_chars)

            admin.set_password = password
            db.session.add(admin)
            db.session.commit()
            return {'username': username, 'password': password, 'state': "Successful Operation!"}, state.eid
        state = STATE_REGISTER_ERR
        return {'state': "username has already existed!"}, state.eid


class AdminPermission(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, location='form')
        self.parser.add_argument('field', type=int, required=True, location='form')
        super(AdminPermission, self).__init__()

    def post(self):
        """
          Set/update the permissions of the administrator role
          ---
          tags:
            - AdminPermission
          parameters:
            - name: body
              in: body
              type: object
              required: true
              schema:
                id: AdminPermission
                properties:
                  username:
                    type: string
                  field:
                    type: int

          responses:
            401:
              description: username does not exist!
            200:
              description: Successful Operation!
        """

        state = STATE_OK
        data = self.parser.parse_args()
        username = data.get("username", None)
        field = data.get("field", None)
        admin = Admin.query.filter_by(username=username).first()
        if admin is None:
            state = STATE_LOGIN_ERR
            return {'state': "username does not exist!"}, state.eid
        # permission 2 indicates that the user is normal admin
        db.session.query(Admin).filter(Admin.username == username).update({"management": field})
        db.session.commit()
        return {'state': "Successful Operation!"}, state.eid


class SendAdminInfo(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(SendAdminInfo, self).__init__()

    def get(self):
        """
          send the administrator information lists
          ---
          tags:
            - SendAdminInfo

          responses:
            200:
              description: Successful Operation!
              schema:
                id: administartorList
                properties:
                  username:
                    type: string
                  management:
                    type: integer
                  confirmed_at:
                    type: string
        """

        # data = self.parser.parse_args()
        # username = data.get("username", None)
        administrators = Admin.query.all()
        administratorList = []
        for admin in administrators:
            if admin.username != 'root':
                administratorList.append(admin.to_json())
        return {'userList': administratorList, 'state': 'Successful Operation!'}, 200


class ChangePassword(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, location='form')
        self.parser.add_argument('originalpassword', type=str, required=True, location='form')
        self.parser.add_argument('newpassword', type=str, required=True, location='form')
        super(ChangePassword, self).__init__()

    def post(self):
        """
          change administrator's password
          ---
          tags:
            - ChangePassword
          parameters:
            - name: body
              in: body
              type: object
              required: true
              schema:
                id: changeInfo
                properties:
                  username:
                    type: string
                  originalpassword:
                    type: string
                  newpassword:
                    type: string
          responses:
            200:
              description: Successful Operation!
            401:
              description: Verification Error!
        """

        data = self.parser.parse_args()
        username = data.get("username", None)
        originalpassword = data.get("originalpassword", None)
        newpassword = data.get("newpassword", None)
        admin = Admin.query.filter_by(username=username).first()
        if admin is None or (not admin.verify_password(originalpassword)):
            state = STATE_LOGIN_ERR
            return {'state': "Verification Error!"}, state.eid
        state = STATE_OK
        admin.set_password = newpassword
        db.session.add(admin)
        db.session.commit()
        return {'state': "Successful Operation!"}, state.eid


class DeleteAdmin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        super(DeleteAdmin, self).__init__()

    def get(self):
        """
          delete the appointed administrator.
          ---
          tags:
            - DeleteAdmin
          parameters:
            - name: body
              in: body
              type: object
              required: true
              schema:
                id: DeleteAdminInfo
                properties:
                  username:
                    type: string

          responses:
            200:
              description: Successful Operation!
            401:
              description: admin does not exist!
        """

        data = self.parser.parse_args()
        username = data.get("username", None)
        admin = Admin.query.filter_by(username=username).first()
        if admin is None:
            state = STATE_LOGIN_ERR
            return {'state': "admin does not exist!"}, state.eid
        state = STATE_OK
        db.session.delete(admin)
        db.session.commit()
        return {'state': "Successful Operation!"}, state.eid


class SendSysParam(Resource):
    def __init__(self):
        super(SendSysParam, self).__init__()

    def get(self):
        """
          Send System Parameters
          ---
          tags:
            - SendSysParam

          responses:
            200:
              description: Successful Operation!
              schema:
                id: SendSysParam
                properties:
                  lowest_prices:
                    type: float
                  top_prices:
                    type: float
                  wait_receive:
                    type: float
                  wait_answer:
                    type: float
                  times_AQ:
                    type: int
                  time_service:
                    type: int
        """

        state = STATE_OK
        sys_param = SystemConfigration.query.all()[0]
        doc = sys_param.to_json()
        return {'doc': doc, 'state': "Successful Operation!"}, state.eid


class SystemConfig(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('lowest_prices', type=int, required=False, location='form')
        self.parser.add_argument('top_prices', type=int, required=False, location='form')
        self.parser.add_argument('wait_receive', type=int, required=False, location='form')
        self.parser.add_argument('wait_answer', type=int, required=False, location='form')
        self.parser.add_argument('times_AQ', type=int, required=False, location='form')
        self.parser.add_argument('time_service', type=int, required=False, location='form')
        super(SystemConfig, self).__init__()

    def post(self):
        """
          Modidy Configure System Parameters
          ---
          tags:
            - SystemConfig
          parameters:
            - name: body
              in: body
              type: object
              required: true
              schema:
                id: sysConfPara
                properties:
                  lowest_prices:
                    type: float
                  top_prices:
                    type: float
                  wait_receive:
                    type: float
                  wait_answer:
                    type: float
                  times_AQ:
                    type: int
                  time_service:
                    type: int

          responses:
            200:
              description: Successful Operation!
        """

        state = STATE_OK
        data = self.parser.parse_args()
        lowest_prices = data.get("lowest_prices", None)
        top_prices = data.get("top_prices", None)
        wait_receive = data.get("wait_receive", None)
        wait_answer = data.get("wait_answer", None)
        times_AQ = data.get("times_AQ", None)
        time_service = data.get("time_service", None)
        sys_param = SystemConfigration.query.all()[0]

        if lowest_prices is not None:
            sys_param.lowest_prices = lowest_prices
        if top_prices is not None:
            sys_param.top_prices = top_prices
        if wait_receive is not None:
            sys_param.wait_receive = wait_receive
        if wait_answer is not None:
            sys_param.wait_answer = wait_answer
        if times_AQ is not None:
            sys_param.times_AQ = times_AQ
        if time_service is not None:
            sys_param.time_service = time_service
        db.session.add(sys_param)
        db.session.commit()
        return {'state': "Successful Operation!"}, state.eid
