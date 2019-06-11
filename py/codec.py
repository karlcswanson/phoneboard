import base64

from channel import Channel

class Codec:
    def __init__(self, ip):
        self.ip = ip
        self.com_status = 'DISCONNECTED'
        self.channels = []
        self.username = ''
        self.password = ''

    def auth_token(self):
        auth = '{}:{}'.format(self.username,self.password)
        return base64.b64encode(str.encode(auth))

    def codec_json(self):
        return { 'ip': self.ip, 'com_status': self.com_status }

    def add_channel(self, cfg):
        self.channels.append(Channel(self, cfg))
