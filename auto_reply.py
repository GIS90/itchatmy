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
import time
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

    _send_unique()
    _send_3_chatroom()

    form_user_name = msg.get('FromUserName')
    search_friend_params = {"me": True}
    me = search_friend_by_params(params=search_friend_params)
    me_user_name = me.get('UserName')

    if form_user_name == me_user_name:
        return
    if not form_user_name:
        return
    if IS_UNIQUE and form_user_name != _get_unique()[1]:
        return

    is_ok = is_bulid_chat(form_user_name)
    if not is_ok:
        rely_msg_text = '主人不在，先由小6陪您聊一会吧！😄'
        itchat.send(rely_msg_text, toUserName=form_user_name)
    else:
        reply_by_ai(msg)


def _get_unique():
    """
    get unique persion at heart
    :return: json data, user name
    """
    search_params = dict()
    unique = search_friend_by_params(nick_name=u'小5', params=search_params)
    unique_user_name = unique.get('UserName')

    return unique, unique_user_name


def _send_unique():
    """
    send message to unique persion
    :return: bool(True or False)
    """
    unique_user_name = _get_unique()[1]

    for i in range(1, 10, 1):
        rely_msg_text = '媳妇😄，我错了❤️，求你了理我 +%s' % i
        itchat.send(rely_msg_text, toUserName=unique_user_name)
        time.sleep(0.5)
    else:
        print 'send ok ...'
        return True


def _send_3_chatroom():
    """
    send message to my unique chatroom
    :return: 
    """
    chat = get_chatroom_by_params(nick_name=u'宝龙山&amp;保康！.宝龙山&amp;保康')
    chat_id = chat.get('UserName')

    for i in range(1, 50, 1):
        time.sleep(0.5)
        rely_msg_text = '嗨皮去啊！😄 +%s' % i
        itchat.send(rely_msg_text, toUserName=chat_id)


def search_friend_by_params(nick_name=None, user_name=None, params={}):
    """
    search friend by params
    :param nick_name: friend nick name
    :param user_name: friend user name
    :param params: qita params
    :return: json data
    
    enums:
        city: [北京，上海 ...]
        sex: 1-男，2-女
        star：[1, 0]
    """
    friends = itchat.get_friends(update=True)
    all = params.get('all') if params else False
    if all:
        return friends

    friend_list = list()
    for friend in friends:
        if not friend:
            continue

        if nick_name and nick_name == friend.get('NickName'):
            return friend
        if user_name and user_name == friend.get('UserName'):
            return friend
        if params.get('me'):
            return friends[0]
        if params.get('sex') and params.get('sex') == friend.get('Sex'):
            friend_list.append(friend)
        if params.get('star') and params.get('star') == friend.get('StarFriend'):
            friend_list.append(friend)
        if params.get('city') and params.get('city') == friend.get('City'):
            friend_list.append(friend)
    else:
        return friend_list


def get_chatroom_by_params(nick_name=None, user_name=None, params={}):
    """
    search chatroom by params
    :param nick_name: chatroom nick name
    :param user_name: chatroom user name
    :param params: qita params
    :return: json data
    
    enums:
        owner: [1, null]
        admin: [1, null]
    """
    chatrooms = itchat.get_chatrooms(update=True)
    all = params.get('all') if params else False
    if all:
        return chatrooms

    chatroom_list = list()
    for chatroom in chatrooms:
        if not chatroom:
            continue

        if nick_name and nick_name == chatroom.get('NickName'):
            return chatroom
        if user_name and user_name == chatroom.get('UserName'):
            return chatroom
        if params.get('admin') and params.get('admin') == chatroom.get('isAdmin'):
            chatroom_list.append(chatroom)
        if params.get('owner') and params.get('owner') == chatroom.get('IsOwner'):
            chatroom_list.append(chatroom)
    else:
        return chatroom_list


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

    resp = requests.post(url=API_ROBOT_URL,
                         headers=headers,
                         data=payload)
    try:
        resp_json = resp.json()
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
