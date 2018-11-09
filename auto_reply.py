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
IS_DEBUG = False


# 处理群聊消息
@itchat.msg_register([TEXT, SHARING, SYSTEM], isGroupChat=True)
def group_text_reply(msg):
    print json.dumps(msg)
    print '%s: %s' % (msg.get('ActualNickName'), msg.get('Text'))

    monitor_chats = [
                     # u'家族群',
                     u'宝龙山&amp;保康！.宝龙山&amp;保康',
                     u'媳妇私房钱'
                    ]
    chat_id_list = list()
    for chat in monitor_chats:
        if not chat:
            continue

        unique_chat = get_chatroom_by_params(nick_name=chat)
        if not unique_chat:
            continue
        unique_chat_id = unique_chat.get('UserName')
        chat_id_list.append(unique_chat_id) if unique_chat_id else None
    else:
        print chat_id_list
        to_user_name = msg.get('ToUserName')
        from_user_name = msg.get('FromUserName')
        is_at = msg.get('isAt') if msg else False
        if is_at or from_user_name in chat_id_list:
            print is_at
            _build_group_auto_reply(msg=msg, chat=from_user_name)
        if IS_DEBUG and to_user_name in chat_id_list:
            print '*' * 100
            print IS_DEBUG
            _build_group_auto_reply(msg=msg, chat=to_user_name)


def _build_group_auto_reply(msg, chat):
    """
    build in group auto reply
    :param msg: message object wx
    :param chat: chat user name
    :return: None
    """
    if not msg or not chat:
        return

    to_nick_name = msg.get('ActualNickName')
    if not to_nick_name:
        to_user_name = msg.get('ToUserName')
        to_user = search_friend_by_params(user_name=to_user_name)
        to_nick_name = to_user.get('NickName')
    rely_msg_text = '@%s %s' % (to_nick_name, reply_by_ai(msg))
    print rely_msg_text,chat
    itchat.send(rely_msg_text, toUserName=chat)


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

    # _send_unique()
    # _send_3_chatroom()

    form_user_name = msg.get('FromUserName')
    # judge is or not me
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
    else:
        rely_msg_text = reply_by_ai(msg)

    itchat.send(rely_msg_text, toUserName=form_user_name)


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
        time.sleep(0.2)
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

    for i in range(1, 5, 1):
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
        if params.get('nicks') and friend.get('NickName') in params.get('nicks'):
            friend_list.append(friend)
        if params.get('users') and friend.get('UserName') in params.get('users'):
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
        if params.get('nicks') and chatrooms.get('NickName') in params.get('nicks'):
            chatroom_list.append(chatroom)
        if params.get('users') and chatrooms.get('UserName') in params.get('users'):
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
    print msg


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
        else:
            rely_msg_text = "小6好像出问题了, 正在通知主人回来抢修"
    except:
        rely_msg_text = "小6没有找到答案😭😭😭, 尝试换个话题吧"
    finally:
        return rely_msg_text


def run(is_unique=False, is_debug=False):
    """
    main method enter
    :param is_unique: is or not unique
    :param is_debug: is or not debug
    :return: None
    """
    init_work()
    global IS_UNIQUE, IS_DEBUG
    IS_UNIQUE = is_unique
    IS_DEBUG = is_debug
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run(True)

if __name__ == "__main__":
    run(is_unique=False, is_debug=False)
