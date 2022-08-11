"""
the model of admin blue print
"""
from utils.ext import db
from flask_security import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class Admin(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    permission = db.Column(db.Integer)
    management = db.Column(db.Integer, default=0)  # 0 indicates that the value is not configured
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

        if "id" in doc:
            del doc['id']

        if "permission" in doc:
            del doc['permission']

        if "password_hash" in doc:
            del doc['password_hash']

        if doc.get('confirmed_at', None):
            doc['confirmed_at'] = doc['confirmed_at'].strftime('%F %T')

        return doc

    @staticmethod
    def insert_root():
        root = Admin.query.filter_by(username='root').first()
        if root is None:
            # 1 indicates that the user is 'root'
            root = Admin(username='root', permission=1, management=1, confirmed_at=datetime.now())
            root.set_password = 'root'
            db.session.add(root)
            db.session.commit()


class SystemConfigration(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    lowest_prices = db.Column(db.Integer)
    top_prices = db.Column(db.Integer)
    wait_receive = db.Column(db.Float)  # max waiting time of receiving order
    wait_answer = db.Column(db.Integer)  # max waiting time of first reply
    times_AQ = db.Column(db.Integer)  # max times of answers and questions
    time_service = db.Column(db.Integer)  # max duration time of answers and questions

    def to_json(self):

        doc = self.__dict__
        if '_sa_instance_state' in doc:
            del doc['_sa_instance_state']

        if "id" in doc:
            del doc['id']

        return doc

    @staticmethod
    def insert_sysparam():

        sys_param = SystemConfigration.query.all()
        if len(sys_param) == 0:
            ini_sys_param = SystemConfigration(lowest_prices=10,
                                               top_prices=100,
                                               wait_receive=10,
                                               wait_answer=10,
                                               times_AQ=10,
                                               time_service=10)  # 1 indicates that the user is 'root'
            db.session.add(ini_sys_param)
            db.session.commit()
