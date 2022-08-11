# -*- coding: utf-8 -*-
"""
the url of order blueprint
"""
from flask import Blueprint
from flask_restful import Api
from .views import *

def get_order_resources():
    order_bp = Blueprint('order', __name__, url_prefix='/api')
    api = Api(order_bp)
    api.add_resource(OrderList, '/orders')
    api.add_resource(AddOrder, '/ask')
    api.add_resource(RefuseAsk, '/refuseask')
    api.add_resource(SelectOrderByAnswerer, '/selectorderbyanswerer')
    api.add_resource(SelectOrderById, '/selectorderbyid')
    api.add_resource(CancelQuestion, '/cancelquestion')
    api.add_resource(CheckOrderList, '/checkorderlist')
    api.add_resource(HiddenCheckOrder, '/hiddencheckorder')
    api.add_resource(CheckOrder, '/checkorder')
    api.add_resource(SelectOrderByQuestioner, '/selectorderbyquestioner')
    api.add_resource(CompleteOrder, '/completeorder')
    api.add_resource(HideOrder, '/hideorder')
    api.add_resource(ModifyOrderState, '/modifyorderstate')
    api.add_resource(FirstAnswer, '/firstanswer')
    return order_bp
