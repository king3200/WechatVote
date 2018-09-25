import datetime

import requests
from django.utils import timezone

from WechatVote import we_settings as settings
from WechatVote.we_settings import wx_offical_token


def wx_get_openid(code):
    wx_response = requests.post(settings.wx_get_user_token_url, {
        'appid': settings.wx_appID,
        'secret': settings.wx_appsecret,
        'code': code,
        'grant_type': 'authorization_code'
    })

    return wx_response.json()


def wx_check_token(token, openid, refresh_token):
    wx_response = requests.get(settings.wx_check_token, {
        'access_token': token,
        'openid': openid
    })

    if wx_response['errcode'] == 0:
        return True
    else:
        #刷新token
        wx_token_refresh_res = requests.get(settings.wx_refresh_token, {
            'appid': settings.wx_appID,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        })
        if hasattr(wx_token_refresh_res.json, 'errcode'):
            return False
        else:
            return wx_token_refresh_res.json()


def wx_get_user_info(access_token, openid):
    wx_userinfo_res = requests.get(settings.wx_user_info_url, {
        'access_token': access_token,
        'openid': openid,
        'lang': 'zh_CN'
    })
    return wx_userinfo_res.json()


def wx_check_subscribe(openid):
    token = wx_get_offical_token()
    print(token)
    res = requests.get(settings.wx_check_subscribe, {
        'access_token': token,
        'openid': openid,
        'lang': 'zh_CN'
    })
    print(res)
    return res.json()['subscribe'] != 0


def wx_get_offical_token():
    expire_time = datetime.timedelta(seconds=7000)
    now = timezone.now()
    if settings.expire_time == None or settings.expire_time + expire_time <= now:
        print('-------------get-new-------token')
        app_id = settings.wx_appID
        secret_id = settings.wx_appsecret
        res = requests.get(wx_offical_token, {
            'appid': app_id,
            'secret': secret_id,

            'grant_type': 'client_credential'
        })
        settings.global_token_cache = res.json()['access_token']
        settings.expire_time = datetime.datetime.now()
        return res.json()['access_token']
    else:
        return settings.global_token_cache
