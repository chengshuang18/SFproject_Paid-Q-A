from utils.ext import my_celery, mail, db
from flask_mail import Message
from flask import current_app
from api.order.models import Order
from api.authentication.model import User, Answerer
from datetime import datetime


@my_celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with current_app.app_context():
        mail.send(msg)


@my_celery.task
def no_accept(order_id):
    """Answerer does not accept order after check"""
    with current_app.app_context():
        get_order = Order.query.filter_by(order_id=order_id).first()
        if get_order.end_mark == 1:
            get_order.end_mark = 5
            questioner = User.query.filter_by(username=get_order.questioner).first()
            questioner.balance += get_order.price
            db.session.commit()

@my_celery.task
def finish_order(order_id):
    """ finish order"""
    """ user balance"""
    get_order = Order.query.filter_by(order_id=order_id).first()
    if get_order.end_mark != 6:
        get_order.end_mark = 6
        answerer = User.query.filter_by(username=get_order.answerer).first()
        answerer.balance += get_order.price
        """ answer statistics"""
        today = datetime.today()
        month = today.month
        answer = Answerer.query.filter_by(username=get_order.answerer).first()
        incomestr = answer.month_income
        tmp = incomestr.split('#')
        tmp[month - 1] = str(float(tmp[month - 1]) + get_order.price)
        answer.month_income = '#'.join(tmp)
        print('#'.join(tmp))
        db.session.commit()


@my_celery.task
def no_answer(order_id):
    with current_app.app_context():
        get_order = Order.query.filter_by(order_id=order_id).first()
        if get_order.first_answer == 0:
            get_order.end_mark = 5
            questioner = User.query.filter_by(username=get_order.questioner).first()
            questioner.balance += get_order.price
            db.session.commit()
