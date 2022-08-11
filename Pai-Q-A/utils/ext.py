# -*- coding: utf-8 -*-
import celery
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail, Message
from celery import Celery
from config import celeryconfig, testceleryconfig


login_manager = LoginManager()
# login_manager.login_view = 'logins.login'

cors = CORS()
db = SQLAlchemy()
mail = Mail()


def make_celery(app_name, config):
    celery = Celery(app_name,
                    broker=config.CELERY_BROKER_URL,
                    backend=config.CELERY_RESULT_BACKEND)
    celery.config_from_object(config)
    return celery


my_celery = make_celery(__name__, config=celeryconfig)
my_test_celery = make_celery(__name__, config=testceleryconfig)
