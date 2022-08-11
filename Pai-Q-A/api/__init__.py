"""
the entrypoint of back-end
"""
from flask import Flask
from utils.ext import db, cors, mail
from api.authentication.url import get_auth_resources
from api.order.url import get_order_resources
from api.admin.url import get_admin_resources
from flasgger import Swagger
from utils.ext import login_manager
import datetime


def register_celery(celery, app):
    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


def create_app(my_celery=None,
               template_folder='../vue/dist',
               static_folder='../vue/dist/static',
               USERNAME='root',
               PASSWORD='123456',
               HOST='127.0.0.1:3306',
               DB='paid-q_a'):

    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s' % (USERNAME, PASSWORD, HOST, DB)
    # 设置每次请求结束后会自动提交数据库中的改动
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True
    # API文档自动生成
    Swagger(app)
    # 解决跨域
    cors.init_app(app, allow_headers='*')
    # mysql init
    db.init_app(app)
    # celery配置
    register_celery(celery=my_celery, app=app)
    # 邮件系统配置
    app.config['MAIL_DEBUG'] = True             # 开启debug，便于调试看信息
    app.config['MAIL_SUPPRESS_SEND'] = False    # 发送邮件，为True则不发送
    app.config['MAIL_SERVER'] = 'smtp.qq.com'
    app.config['MAIL_USE_SSL'] = True           # 重要，qq邮箱需要使用SSL
    app.config['MAIL_USE_TLS'] = False          # 不需要使用TLS
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = '3247574125@qq.com'
    app.config['MAIL_PASSWORD'] = 'batklibjtjcocjfb'
    app.config['MAIL_DEFAULT_SENDER'] = '3247574125@qq.com'
    mail.init_app(app)
    # 临时激活一个请求环境。在这个 环境中可以像以视图函数中一样操作 request 、g 和 session 对象
    with app.test_request_context():
        db.create_all()
    # 蓝图功能, 注册api url
    app.register_blueprint(get_auth_resources())
    app.register_blueprint(get_order_resources())
    app.register_blueprint(get_admin_resources())
    # login 管理
    login_manager.remember_cookie_duration = datetime.timedelta(seconds=60)
    login_manager.init_app(app)
    return app
