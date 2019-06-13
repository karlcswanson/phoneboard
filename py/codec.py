import base64
import urllib.request
import json
import logging

from channel import Channel

class Codec:
    def __init__(self, ip):
        self.ip = ip
        self.com_status = 'DISCONNECTED'
        self.channels = []
        self.username = 'admin'
        self.password = 'admin'

    def auth_token(self):
        auth = '{}:{}'.format(self.username,self.password)
        return base64.b64encode(str.encode(auth)).decode('utf-8')

    def codec_json(self):
        channels = []
        for channel in self.channels:
            channels.append(channel.ch_json())
        return {
            'ip': self.ip, 'com_status': self.com_status, 'channels': channels
        }

    def add_channels(self, cfg):
        for chan in cfg['channels']:
            self.channels.append(Channel(self, chan))

    def load_json(self, path):
        url = 'http://' + self.ip + path
        print(url)
        req = urllib.request.Request(url)

        req.add_header('authorization','Basic {}'.format(self.auth_token()))
        try:
            resp = urllib.request.urlopen(req)
            if resp.getcode() == 200:
                return json.loads(resp.read())
        except:
            logging.warning('URL did not return 200')
            return None

    def get_channel(self, channel):
        for ch in self.channels:
            if ch.channel == channel:
                return ch

    def get_vu(self):
        path = '/cm/getEvent'
        try:
            out = self.load_json(path)

            if out['type'] == 'vuLevel':
                ch_l = self.get_channel('left')
                ch_r = self.get_channel('right')
                ch_l.vu = out['ml0']
                ch_r.vu = out['mr1']
        except:
            logging.info("NO VU 4U!")
