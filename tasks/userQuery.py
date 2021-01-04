# Thread that detects when the user was sign up and appears in the DB

import threading
import time
import requests
from api.mongodb import MongoDB
import constants as const


class RepeatEvery(threading.Thread):
    def __init__(self, interval, *args, **kwargs):
        threading.Thread.__init__(self)
        self.mongo = MongoDB()
        self.interval = interval  # seconds between calls
        self.args = args          # optional positional argument(s) for call
        self.kwargs = kwargs      # optional keyword argument(s) for call
        self.runnable = True

    def run(self):
        while self.runnable:
            self.query_userid(*self.args, **self.kwargs)
            time.sleep(self.interval)

    def stop(self):
        self.runnable = False

    def display_menu(self):
        print("Sending message to chat id {} user id {}".format(const.chatinfo['chatid'], const.chatinfo['userid']))
        url = 'https://graph.facebook.com/v7.0/me/messages?access_token=' + const.FB_TOKEN
        json = const.json_menu
        json['recipient']['id'] = const.chatinfo['userid']
        print(json)
        x = requests.post(url, json=json)
        print(x.text)

    def query_userid(self, userid):
        if self.mongo.get_user_by_id(userid):
            self.display_menu()
            self.stop()
