# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
mingliang.gao
usage:


base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2018/10/22"
    __mail__ = "mingliang.gao@qunar.com"
------------------------------------------------
"""
import os
import json
import datetime


def is_bulid_chat(user_name, minute=30):
    """
    judge is or not build the user chat room over half an hour
    :param user_name: unique user name
    :param minute: minute value
    :return: bool(true of false)
    """
    flag = False
    if not user_name:
        return flag

    refile = get_default_refile()
    now_value = get_now_date()
    with open(refile, mode='r') as f:
        records = f.readline()

    if records:
        json_records = json.loads(records, encoding='utf-8')
        user_value = json_records.get(user_name)
        if user_value:
            user_value_d = s2d(user_value)
            seconds = (now_value - user_value_d).seconds
            if seconds <= (minute * 60):
                flag = True
    else:
        json_records = dict()

    json_records[user_name] = d2s(now_value)
    res = json.dumps(json_records, encoding='utf-8')
    with open(refile, mode='w') as f:
        f.write(res)

    return flag


def s2d(s, fmt="%Y-%m-%d %H:%M:%S"):
    """
    time string transfer to date time
    :param s: string time
    :param fmt: time formatter
    :return: datetime
    """
    return datetime.datetime.strptime(s, fmt)


def d2s(d, fmt="%Y-%m-%d %H:%M:%S"):
    """
    date time transfer to string time
    :param d: date time
    :param fmt: time formatter
    :return: string time
    """
    return d.strftime(fmt)


def get_now_date():
    """
    get current date time
    :return: date time
    """
    return datetime.datetime.now()


def init_work():
    """
    initialize the chat user time file
    :return: None
    """
    user_file = get_default_refile()
    if os.path.exists(user_file) and os.path.isfile(user_file):
        return
    open(user_file, 'a').close()
    print 'init work of record user chat file is ok'


def get_default_refile():
    """
    default record file
    :return: file
    """
    cur_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    user_file = cur_path + '/record_user.log'
    return user_file


