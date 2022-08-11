# -*- coding: utf-8 -*-
""" manage.py runserver -h 127.0.0.1 -p 8888 --debug """
from api import create_app
from flask_migrate import Migrate, MigrateCommand, upgrade
from flask_script import Manager
from api.admin.model import Admin, SystemConfigration
from utils.ext import db, my_celery
import logging
from flask.helpers import send_file


app = create_app(my_celery=my_celery,
                template_folder='../vue/dist',
                static_folder='../vue/dist/static',
                USERNAME='pai-q-a-mysql',
                PASSWORD='123456',
                HOST='Pai-Q-A-MySQL.AutoEng.secoder.local:3306',
                DB= 'docker_mysql')
# app = create_app(my_celery=my_celery)
manager = Manager(app)
migrate = Migrate(app, db)

# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade
manager.add_command('db', MigrateCommand)


@manager.command
def insert_basic_param():
    # upgrade()
    Admin.insert_root()
    SystemConfigration.insert_sysparam()


@manager.app.route('/')
def index_client():
    return send_file('../vue/dist/index.html')


@manager.app.route('/logout')
def logout():
    from flask_security import logout_user
    logout_user()
    return "logout ok"


if __name__ == '__main__':

    # 通过url_map可以查看整个flask中的路由信息
    print(app.url_map)
    # 启动flask程序
    # app.run(debug=True)
    # python manage.py  runserver -h 0.0.0.0 -p 8888
    manager.run()
