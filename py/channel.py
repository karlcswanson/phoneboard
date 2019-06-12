import time

import codec


class Channel:
    def __init__(self, codec, cfg):
        self.codec = codec
        self.title = cfg['title']
        self.channel = cfg['channel']
        self.uri = cfg['uri']
        self.timestamp = time.time() - 60
        self.slot = cfg['slot']
        self.hook_status = 'ON_HOOK'

    def update_hook_status(self):
        path = '/ve/channel/ahStatus?ch=' + self.channel
        out = self.codec.load_json(path)
        if out['oh']:
            self.hook_status = 'OFF_HOOK'
        else:
            self.hook_status = 'ON_HOOK'

    def call(self):
        path = '/ve/channel/call?ch={}&uri={}'.format(self.channel, self.uri)
        out = self.codec.load_json(path)
        print(out)

    def drop(self):
        path = '/ve/channel/line?ch={}&oh=false'.format(self.channel)
        out = self.codec.load_json(path)
        print(out)
