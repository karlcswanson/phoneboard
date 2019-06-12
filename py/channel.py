import time
import logging

import codec


class Channel:
    def __init__(self, codec, cfg):
        self.codec = codec
        self.name = cfg['name']
        self.channel = cfg['channel']
        self.uri = cfg['uri']
        self.timestamp = time.time() - 60
        self.slot = cfg['slot']
        self.hook_status = 'ON_HOOK'
        self.call_start = time.time() - 60
        self.vu = 0


    def set_hook_status(self, status):
        if self.hook_status == 'OFF_HOOK' and status == 'ON_HOOK':
            delta = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.call_start))
            logging.info('{} is on hook after {}'.format(self.name, delta))

        if status == 'ON_HOOK':
            self.call_start = time.time()
            self.hook_status = 'ON_HOOK'


        if status == 'OFF_HOOK':
            self.call_start = time.time()
            self.hook_status = 'OFF_HOOK'

        logging.info('{} is {}'.format(self.name, self.hook_status))

    def get_hook_status(self):
        path = '/ve/channel/ahStatus?ch=' + self.channel
        out = self.codec.load_json(path)
        if out['oh']:
            self.set_hook_status('OFF_HOOK')
        else:
            self.set_hook_status('ON_HOOK')


    def call(self):
        path = '/ve/channel/call?ch={}&uri={}'.format(self.channel, self.uri)
        out = self.codec.load_json(path)
        if 'call' in out:
            self.set_hook_status('OFF_HOOK')
        print(out)

    def drop(self):
        path = '/ve/channel/line?ch={}&oh=false'.format(self.channel)
        out = self.codec.load_json(path)
        if out['oh'] == 0:
            self.set_hook_status('ON_HOOK')
        print(out)


    def ch_json(self):
        return {
            'name': self.name, 'status': self.hook_status, 'slot': self.slot,
            'vu': self.vu
        }
