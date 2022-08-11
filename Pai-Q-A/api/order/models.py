"""
the model of order
"""
from utils.ext import db
from datetime import datetime


class Order(db.Model):
    # 定义创建的表名
    __tablename__ = 'orders'
    # 定义字段
    # primary_key=True 声明主键  unique=True 值唯一  nullable=False 非空
    order_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255))
    questioner = db.Column(db.String(255))
    answerer = db.Column(db.String(255))
    content = db.Column(db.String(255))
    answer_content = db.Column(db.String(255))
    end_mark = db.Column(db.Integer)
    price = db.Column(db.Float)
    first_answer = db.Column(db.Integer, default=0)
    # 审核系统参数
    field = db.Column(db.Integer)
    check_mark = db.Column(db.Integer)
    confirmed_at = db.Column(db.DateTime(), default=datetime.now())  # 订单生成时间
    receive_at = db.Column(db.DateTime())  # 回答者接单时间
    time_qa = db.Column(db.Integer, default=0)

    def __init__(self, title, questioner, answerer, price, field, content, end_mark, check_mark):
        self.title = title
        self.questioner = questioner
        self.answerer = answerer
        self.content = content
        self.end_mark = end_mark
        self.check_mark = check_mark
        self.price = price
        self.field = field

    def __repr__(self):
        return '<Order: %s>' % self.title

    def to_check_json(self):
        doc = self.__dict__
        if '_sa_instance_state' in doc:
            del doc['_sa_instance_state']

        if 'end_mark' in doc:
            del doc['end_mark']

        if 'confirmed_at' in doc:
            del doc['confirmed_at']

        if doc.get('receive_at', None):
            del doc['receive_at']

        if doc.get('time_qa', None):
            del doc['time_qa']

        return doc


def create_table():
    # 删除表
    db.drop_all()
    # 创建表
    db.create_all()
    order1 = Order(title='question1', questioner='Alice', answerer='Bob',
                   content='q1', end_mark=0, check_mark=1, price=19.9, field=2)
    order2 = Order(title='question2', questioner='Bob', answerer='Carol',
                   content='q2', end_mark=1, check_mark=1, price=19.9, field=2)
    order3 = Order(title='question3', questioner='Alice', answerer='Carol',
                   content='q3', end_mark=0, check_mark=1, price=19.9, field=2)
    db.session.add_all([order1, order2, order3])
    db.session.commit()
