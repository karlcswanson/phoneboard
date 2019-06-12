import base64
import urllib.request
import json

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
        return { 'ip': self.ip, 'com_status': self.com_status }

    def add_channels(self, cfg):
        for chan in cfg['channels']:
            self.channels.append(Channel(self, chan))

    def load_json(self, path):
        url = 'http://' + self.ip + path
        print(url)
        req = urllib.request.Request(url)

        req.add_header('authorization','Basic {}'.format(self.auth_token()))
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
