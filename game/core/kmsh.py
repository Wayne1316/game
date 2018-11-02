# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime, date, time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

from zeep import Client

from core.logger import auth_logger
from users.models import (
    Profile,
    UserMail
)


class UserNotExistsException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = 'user account not exists'
        super(UserNotExistsException, self).__init__(*args, **kwargs)


class PasswordInvaildException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = 'invaild password'
        super(PasswordInvaildException, self).__init__(*args, **kwargs)


class AccountExpiredException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = 'user account was expired'
        super(AccountExpiredException, self).__init__(*args, **kwargs)


class Service(object):
    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)

    client = Client(settings.SOAP_URL)

    @staticmethod
    def user_format(user):
        return {
            'error_code': user['result'],
            'error_msg': user['msg'],
            'username': user['reader01'],
            'password': user['reader13'],
            'name': user['reader02'],
            'school': user['reader72'],
            'tel': user['reader07'],
            'birth': user['reader03'],
            'mail1': user['reader14'],
            'mail2': user['reader60'],
            'phone1': user['reader61'],
            'phone2': user['reader62'],
            'department': user['reader26'],
            'identity': user['reader29'],
            'expired': user['yxrq']
        }

    def get_user(self, username, password):
        response = self.client.service.loginJSON(username, password)
        res = json.loads(response, encoding='utf-8')[0]
        return self.user_format(res)


@transaction.atomic
def resister_or_update(user):
    def user_exists():
        return Profile.objects.filter(uid__username=user['username']).count() > 0

    def update():
        # Update profile
        row = Profile.objects.filter(uid__username=user['username'])[0]
        row.phone = user['tel']
        row.save()

        get_user_model().objects.filter(pk=row.uid.pk).update(first_name=user['name'])

        # Update user
        obj = get_user_model().objects.get(id=row.pk)
        obj.set_password(user['password'])
        obj.save()
        update_mail(obj, mails=[user['mail1'], user['mail2']])

    def register():
        # add new user
        obj = get_user_model().objects.create_user(user['username'], password=user['password'], first_name=user['name'])
        Profile.objects.create(uid=obj, phone=user['tel'])
        update_mail(obj, mails=[user['mail1'], user['mail2']])

    def update_mail(uid, mails):
        # Sync user mail list
        # Delete not in list mail
        UserMail.objects.filter(uid=uid).exclude(email=mails).delete()
        # sync username
        for mail in mails:
            UserMail.objects.update_or_create(uid=uid, email=mail)

    if user_exists():
        update()
        auth_logger().info('user <{username}> update'.format(username=user['username']))
    else:
        register()
        auth_logger().info('user <{username}> register'.format(username=user['username']))


def authenticate(username, password):
    service = Service()
    user = service.get_user(username, password)
    if user['error_code'] == '2':
        raise UserNotExistsException()
    elif user['error_code'] == '3':
        raise PasswordInvaildException()
    elif datetime.strptime(user['expired'], "%Y-%m-%d") < datetime.combine(date.today(), time()):
        raise AccountExpiredException()
    resister_or_update(user)
