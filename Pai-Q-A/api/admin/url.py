# -*- coding: utf-8 -*-
"""
the url of admin blueprint
"""
from flask import Blueprint
from flask_restful import Api
from .view import *


def get_admin_resources():
    admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
    api = Api(admin_bp)
    api.add_resource(Login, '/login')
    api.add_resource(AddAdmin, '/addadmin')
    api.add_resource(AdminPermission, '/adminpermission')
    api.add_resource(SendAdminInfo, '/sendadmininfo')
    api.add_resource(ChangePassword, '/changepassword')
    api.add_resource(DeleteAdmin, '/deleteadmin')
    api.add_resource(SystemConfig, '/systemconfig')
    api.add_resource(SendSysParam, '/sendsysparam')
    return admin_bp
