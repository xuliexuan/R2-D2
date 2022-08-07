#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

# Company id、key
CORP_ID = 'ww6da4d28ed4760bd7' # change to user id
CORP_SECRET = 'AoB4gJL2ZB6ogNBwN_8ZOEsYb38nOPS1nNTmifUOTa0' # change to user app secret
AGENT_ID = 1000002 #change to user app id, must digital type, not string type

# wechat class
class WeChatAPI():
    def __init__(self, corp_id, corp_secret):
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.update_token()

    # base on user id and secret, get token
    def get_token(self):
        token_api = (
                        'https://qyapi.weixin.qq.com/cgi-bin/gettoken?' +
                        f'corpid={self.corp_id}&corpsecret={self.corp_secret}'
                    )
        try:
            response = requests.get(token_api, timeout=10)
        except:
            print('Timeout, did not get access_token')
            return 'error'

        # print(response.json()['access_token'])
        return response.json()['access_token']

    def update_token(self):
        self.access_token = self.get_token()
        self.send_api = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?' + f'access_token={self.access_token}'

    def send_text_message(self, title, text, agent_id=AGENT_ID, touser="@all"):
        data = json.dumps({
            "touser" : touser,
            "msgtype" : "text",
            "agentid" : agent_id,
            "text" : {
                "content" : title + '\n\n' + text
            },
            "safe":0
        })
        try:
            response = requests.post(self.send_api, data=data, timeout=10).json()
        except:
            print('Timeout, Do not send message')
            return
        if response['errcode']==42001 or response['errcode']==40014:
            self.update_token()
            self.send_text_message(title, text, agent_id=agent_id, touser=touser)
        elif response['errcode'] == 0:
            print(title, 'Send Successfully!')
        else:
            print('Send Failed!')
            print('data: ', data)
            print('response: ', response)
            print('token: ', self.access_token)

if __name__ == '__main__':
    wechat_api = WeChatAPI(CORP_ID, CORP_SECRET)
    wechat_api.send_text_message('hello world!', '@all')
