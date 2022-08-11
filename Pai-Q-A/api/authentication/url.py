# -*- coding: utf-8 -*-
"""
the url of authentication blueprint
"""
from flask import Blueprint
from flask_restful import Api
from .view import *


def get_auth_resources():
    auth_bp = Blueprint('auth', __name__, url_prefix='/api')
    api = Api(auth_bp)
    api.add_resource(Login, '/login')
    api.add_resource(Register, '/register')
    api.add_resource(Upgrade, '/upgrade')
    api.add_resource(SendAnsInfo, '/sendansinfo')
    api.add_resource(WalletManagement, '/walletmanagement')
    api.add_resource(genUserSig, '/genusersig')
    api.add_resource(SendUserList, '/senduserlist')
    api.add_resource(AnswererInfo, '/answererinfo')
    api.add_resource(ModifyUserInfo, '/modifyuserinfo')
    api.add_resource(ModifyPassword, '/modifypassword')
    api.add_resource(SendVerificationCode, '/sendverificationcode')
    api.add_resource(FindPassword, "/findpassword")
    api.add_resource(GetUserMsg, "/getusermsg")
    api.add_resource(SendAnsIncome, "/sendansincome")
    api.add_resource(ModifyAnsIncome, "/modifyansincome")
    return auth_bp
