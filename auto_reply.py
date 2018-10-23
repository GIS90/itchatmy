# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:

usage:


base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2018/10/19"
    __mail__ = "mingliang.gao@qunar.com"
------------------------------------------------
"""
import sys
import json
import itchat
import requests
from itchat.content import *
from utiles import is_bulid_chat, init_work

reload(sys)
sys.setdefaultencoding('utf8')

IS_UNIQUE = False


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def handler_text_msg(msg):
    """
    auto reply messages [text, map, card, note, sharing] by friend or group
    :param msg: wx message (dict)
    :return: text message
    """
    print '- = ' * 22
    print msg.get('Type')
    print json.dumps(msg)

    user_name = msg.get('FromUserName')
    if not user_name:
        pass
    if IS_UNIQUE and user_name != '@91bc6199f31c889e141026a9ee1d790b1658811a285362c5edd96962b668473a':
        pass

    is_ok = is_bulid_chat(user_name)
    if not is_ok:
        rely_msg_text = '主人不在，先由小6陪您聊一会吧！😄'
        itchat.send(rely_msg_text, toUserName=user_name)
    else:
        reply_by_ai(msg)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def hander_file_msg(msg):
    """
    auto reply messages [picture, recording, attachment, video] by friend or group
    :param msg: wx message(dict)
    :return: message
    """
    print '- * ' * 22
    print type(msg)
    print msg.get('Type')



def reply_by_ai(msg):
    """
    auto reply by ai robot
    :param msg: message body by wx friend
    :return: send message
    """
    user_name = msg.get('FromUserName')
    msg_type = msg.get('Type')
    msg_text = msg.get('Text')
    API_ROBOT_URL = 'http://openapi.tuling123.com/openapi/api/v2'
    API_KEY = '65d96c7612e14a3ba8c6d43fa7a84111'
    USER_ID = '113972'

    payload = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": msg_text
            }
        },
        "userInfo": {
            "apiKey": API_KEY,
            "userId": USER_ID
        }
    }
    payload = json.dumps(payload)
    headers = {"Content-Type": "application/json"}
    print payload
    resp = requests.post(url=API_ROBOT_URL,
                         headers=headers,
                         data=payload)
    try:
        resp_json = resp.json()
        print resp_json
        code = resp_json.get('intent').get('code')
        if resp.status_code == 200 and code >= 10000:
            result = resp_json.get('results')[0]
            rely_msg_text = result.get('values').get('text')
            itchat.send(rely_msg_text, toUserName=user_name)
        else:
            rely_msg_text = "小6好像出问题了, 正在通知主人回来抢修"
            itchat.send(rely_msg_text, toUserName=user_name)
    except:
        rely_msg_text = "小6没有找到答案😭😭😭, 尝试换个话题吧"
        itchat.send(rely_msg_text, toUserName=user_name)


def run(is_unique=False):
    """
    main method enter
    :return: None
    """
    init_work()
    global IS_UNIQUE
    IS_UNIQUE = is_unique
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run(True)

if __name__ == "__main__":
    run(is_unique=False)
