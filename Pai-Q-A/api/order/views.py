"""
the view of order blueprint
"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from marshmallow import Schema
from marshmallow import fields
from api.authentication.model import User, Answerer
from .models import Order
from utils.ext import db
from utils.errorCode import *
import base64
from api.admin.model import SystemConfigration
from utils.task import no_accept, finish_order, no_answer
from datetime import datetime


class OrderSchema(Schema):
    class Meta(Schema.Meta):
        model = Order
        sql_session = db.session

    order_id = fields.Number()
    title = fields.String()
    questioner = fields.String()
    answerer = fields.String()
    content = fields.String()
    answer_content = fields.String()
    end_mark = fields.Number()
    field = fields.Number()
    check_mark = fields.Number()
    confirmed_at = fields.DateTime()
    receive_at = fields.DateTime()
    time_qa = fields.Number()
    price = fields.Float()
    first_answer = fields.Integer()


class OrderList(Resource):
    def __init__(self):
        super(OrderList, self).__init__()

    def get(self):
        """
         return order list
         ---
         tags:
           - OrderList
         responses:
           200:
             description: Successful Operation!
             schema:
                properties:
                  order_id:
                    type: integer
                  title:
                    type: string
                  questioner:
                    type: string
                  answerer:
                    type: string
                  content:
                    type: string
                  answer_content:
                    type: string
                  end_mark:
                    type: integer
                  field:
                    type: integer
                  check_mark:
                    type: integer
                  confirmed_at:
                    type: datetime
                  receive_at:
                    type: datetime
                  time_qa:
                    type: integer
       """

        get_order = Order.query.all()
        order_schema = OrderSchema(many=True)
        orders = order_schema.dump(get_order)
        return make_response(jsonify({"orders": orders}), 200)


class AddOrder(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, required=True, location='form')
        self.parser.add_argument('questioner', type=str, required=True, location='form')
        self.parser.add_argument('answerer', type=str, required=True, location='form')
        self.parser.add_argument('content', type=str, required=True, location='form')
        super(AddOrder, self).__init__()

    def post(self):
        """
              add order when ask question
              ---
              tags:
                - AddOrder
              parameters:
                - name: body
                  in: body
                  type: object
                  required: true
                  schema:
                    properties:
                      title:
                        type: string
                      questioner:
                        type: string
                      answerer:
                        type: string
                      content:
                        type: string

              responses:
                201:
                  description: ASK SUCCESS

            """
        data = self.parser.parse_args()
        title = data.get('title', None)
        questioner = data.get('questioner', None)
        answerer = data.get('answerer', None)
        content = data.get('content', None)
        answerer_ = Answerer.query.filter_by(username=answerer).first()
        order = Order(title=title,
                      questioner=questioner,
                      answerer=answerer,
                      content=content,
                      price=answerer_.price,
                      field=answerer_.field,
                      end_mark=1,
                      check_mark=1)
        db.session.add(order)
        db.session.commit()
        state = STATE_CREATE_OK
        return {'state': "ASK SUCCESS"}, state.eid


class RefuseAsk(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=int, required=True, location='form')
        super(RefuseAsk, self).__init__()

    def post(self):
        """
            update end mark if refuse to answer question
            ---
            tags:
              - RefuseAsk
            parameters:
              - name: body
                in: body
                type: object
                required: true
                schema:
                  id: refuse
                  properties:
                    order_id:
                      type: integer

            responses:
              200:
                description: Successful Operation!

        """
        data = self.parser.parse_args()
        order_id = data.get('order_id', None)
        db.session.query(Order).filter(Order.order_id == order_id).update({"end_mark": 5})
        db.session.commit()
        state = STATE_OK
        return {'state': "Refuse Completed"}, state.eid


class SelectOrderByAnswerer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('answerer', type=str)
        super(SelectOrderByAnswerer, self).__init__()

    def get(self):
        data = self.parser.parse_args()
        answerer = data.get('answerer', None)
        get_order = Order.query.filter_by(answerer=answerer)
        if get_order is None:
            state = STATE_EmptyData_ERR
            return {'state': "Order Not Exist!"}, state.eid
        order_schema = OrderSchema(many=True)
        orders = order_schema.dump(get_order)
        for order in orders:
            order['questioner_photo'] = str(base64.b64encode(User.query.filter_by(username=order['questioner']).first().photo))
        orders.append({"answerer_photo": str(base64.b64encode(User.query.filter_by(username=answerer).first().photo))})
        return make_response(jsonify({"orders": orders}), 200)


class SelectOrderById(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=int)
        super(SelectOrderById, self).__init__()

    def get(self):
        data = self.parser.parse_args()
        order_id = data.get('order_id', None)
        get_order = Order.query.filter_by(order_id=order_id)
        order_schema = OrderSchema(many=True)
        orders = order_schema.dump(get_order)
        return make_response(jsonify({"orders": orders}), 200)


class CancelQuestion(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=int, required=True, location='form')
        super(CancelQuestion, self).__init__()

    def post(self):
        """
            update end mark if cancel to question for quizzer
            ---
            tags:
              - CancelQuestion
            parameters:
              - name: body
                in: body
                type: object
                required: true
                schema:
                  id: refuse
                  properties:
                    order_id:
                      type: integer

            responses:
              200:
                description: Successful Operation!
              402:
                description: order does not exist!

        """
        data = self.parser.parse_args()
        order_id = data.get('order_id', None)
        if db.session.query(Order).filter(Order.order_id == order_id).first() is not None:
            db.session.query(Order).filter(Order.order_id == order_id).update({"end_mark": 0})
            db.session.commit()
            state = STATE_OK
            return {'state': "Successful Operation!"}, state.eid
        state = STATE_EmptyData_ERR
        return {'state': "order does not exist!"}, state.eid


class CheckOrderList(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('field', type=int, required=True)
        super(CheckOrderList, self).__init__()

    def get(self):
        """
          send the check order lists
          ---
          tags:
            - CheckOrderList
          parameters:
            - name: params
              in: params
              type: object
              required: True
              schema:
                id: OrderField
                properties:
                  field(100表示root, 0表示非审核者管理员):
                    type: integer

          responses:
            200:
              description: Successful Operation!
              schema:
                id: administartorList
                properties:
                  order_id:
                    type: integer
                  title:
                    type: string
                  content:
                    type: string
                  questioner:
                    type: string
                  answerer:
                    type: string
                  check_mark:
                    type: integer
                  field:
                    type: string
        """

        data = self.parser.parse_args()
        field = data.get('field', None)
        OrderList = Order.query.all()
        DispalyOrderList = []
        if field == 100:  # 100表示为root
            for order in OrderList:
                if order.check_mark != 4:
                    DispalyOrderList.append(order.to_check_json())
        elif field == 0:
            return {'userList': [], 'state': 'Successful Operation!'}, 200
        else:
            for order in OrderList:
                if order.check_mark != 4 and order.field == (field - 1):
                    DispalyOrderList.append(order.to_check_json())
        return {'userList': DispalyOrderList, 'state': 'Successful Operation!'}, 200


class HiddenCheckOrder(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=int, required=True, location='form')
        super(HiddenCheckOrder, self).__init__()

    def post(self):
        """
          hide the appointed checkorder.
          ---
          tags:
            - HiddenCheckOrder
          parameters:
            - name: body
              in: body
              type: object
              required: True
              schema:
                id: OrderId
                properties:
                  order_id:
                    type: integer

          responses:
            200:
              description: Successful Operation!
        """
        data = self.parser.parse_args()
        order_id = data.get('order_id', None)
        get_order = Order.query.filter_by(order_id=order_id)
        get_order.update({"check_mark": 4})
        db.session.commit()
        state = STATE_OK
        return {'state': "Successful Operation!"}, state.eid


class CheckOrder(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=int, required=True, location='form')
        self.parser.add_argument("check_mark", type=int, required=True, location='form')
        super(CheckOrder, self).__init__()

    def post(self):
        """
          check the appointed checkorder.
          ---
          tags:
            - CheckOrder
          parameters:
            - name: body
              in: body
              type: object
              required: True
              schema:
                id: OrderIdandCheckInfo
                properties:
                  order_id:
                    type: integer
                  check_mark:
                    type: integer

          responses:
            200:
              description: Successful Operation!
        """

        data = self.parser.parse_args()
        order_id = data.get('order_id', None)
        check_mark = data.get('check_mark', None)
        get_order = Order.query.filter_by(order_id=order_id).first()
        get_order.check_mark = check_mark
        get_order.confirmed_at = datetime.now()
        db.session.commit()
        if check_mark == 2:
            sys_param = SystemConfigration.query.all()[0]
            no_accept.apply_async(args=[order_id], countdown=sys_param.wait_receive * 60)  # 如果按照小时 需要乘以3600
        state = STATE_OK
        return {'state': "Successful Operation!"}, state.eid


class SelectOrderByQuestioner(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('questioner', type=str)
        super(SelectOrderByQuestioner, self).__init__()

    def get(self):
        """
             return order list selected by questioner
             ---
             tags:
               - SelectOrderByQuestioner
             parameters:
              - name: body
                in: body
                type: object
                required: true
                schema:
                  properties:
                    questioner:
                      type: string
             responses:
               200:
                 description: Successful Operation!
                 schema:
                    properties:
                      order_id:
                        type: integer
                      title:
                        type: string
                      questioner:
                        type: string
                      answerer:
                        type: string
                      content:
                        type: string
                      answer_content:
                        type: string
                      end_mark:
                        type: integer
                      field:
                        type: integer
                      check_mark:
                        type: integer
                      confirmed_at:
                        type: datetime
                      receive_at:
                        type: datetime
                      time_qa:
                        type: integer
           """

        data = self.parser.parse_args()
        questioner = data.get('questioner', None)
        get_order = Order.query.filter_by(questioner=questioner)
        if get_order is None:
            state = STATE_EmptyData_ERR
            return {'state': "Order Not Exist!"}, state.eid
        order_schema = OrderSchema(many=True)
        orders = order_schema.dump(get_order)
        for order in orders:
            order['answerer_photo'] = str(base64.b64encode(Answerer.query.filter_by(username=order['answerer']).first().photo))
        orders.append({"questioner_photo": str(base64.b64encode(User.query.filter_by(username=questioner).first().photo))})
        return make_response(jsonify({"orders": orders}), 200)


class CompleteOrder(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=int)

    def get(self):
        """
            complete order
            ---
            tags:
              - CompleteOrder
            parameters:
              - name: body
                in: body
                type: object
                required: true
                schema:
                  properties:
                    order_id:
                      type: integer

            responses:
              200:
                description: Successful Operation!

        """
        data = self.parser.parse_args()
        order_id = data.get('order_id', None)
        db.session.query(Order).filter(Order.order_id == order_id).update({"end_mark": 3})
        db.session.commit()
        state = STATE_OK
        finish_order.apply_async(args=[order_id], countdown=60)
        return {'state': "Successful Operation!"}, state.eid


class HideOrder(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=int)

    def get(self):
        """
            hide order
            ---
            tags:
              - HideOrder
            parameters:
              - name: body
                in: body
                type: object
                required: true
                schema:
                  properties:
                    order_id:
                      type: integer

            responses:
              200:
                description: Successful Operation!
        """

        data = self.parser.parse_args()
        order_id = data.get('order_id', None)
        db.session.query(Order).filter(Order.order_id == order_id).update({"end_mark": 4})
        db.session.commit()
        state = STATE_OK
        return {'state': "Successful Operation!"}, state.eid


class ModifyOrderState(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=int)
        self.parser.add_argument('end_mark', type=int)

    def get(self):
        """
            modify order state
            ---
            tags:
              - ModifyOrderState
            parameters:
              - name: body
                in: body
                type: object
                required: true
                schema:
                  properties:
                    order_id:
                      type: integer
                    end_mark:
                      type: integer

            responses:
              200:
                description: Successful Operation!

        """

        data = self.parser.parse_args()
        order_id = data.get('order_id', None)
        end_mark = data.get('end_mark', None)
        db.session.query(Order).filter(Order.order_id == order_id).update({"end_mark": end_mark})
        db.session.commit()
        state = STATE_OK
        get_order = Order.query.filter_by(order_id=order_id).first()
        if end_mark == 2 and get_order.first_answer == 0:
            sys_param = SystemConfigration.query.all()[0]
            get_order.receive_at = datetime.now()
            no_answer.apply_async(args=[order_id], countdown=sys_param.wait_answer*60)  # 如果按照小时 需要乘以3600
        return {'state': "Successful Operation!"}, state.eid


class FirstAnswer(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=int)
        self.parser.add_argument('questioner', type=str)
        self.parser.add_argument('answerer', type=str)
        super(FirstAnswer, self).__init__()

    def get(self):
        """
          modify the FirstAnswer
          ---
          tags:
            - FirstAnswer
          parameters:
            - name: body
              in: body
              type: object
              required: True
              schema:
                id: OrderId
                properties:
                  order_id:
                    type: integer

          responses:
            200:
              description: Successful Operation!
            402:
              description: order does not exist!
        """

        data = self.parser.parse_args()
        order_id = data.get('order_id', None)
        questioner = data.get('questioner', None)
        answerer = data.get('answerer', None)
        get_order = Order.query.filter_by(order_id=order_id).first()
        if get_order is None:
            state = STATE_EmptyData_ERR
            return {'state': "order does not exist!"}, state.eid
        if get_order.first_answer == 0 and get_order.end_mark == 2 and get_order.questioner == questioner and get_order.answerer == answerer:
            get_order.first_answer = 1
            sys_param = SystemConfigration.query.all()[0]
            finish_order.apply_async(args=[order_id], countdown=sys_param.time_service*60)
            db.session.commit()
        state = STATE_OK
        return {'state': "Successful Operation!"}, state.eid
